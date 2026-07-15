from __future__ import annotations

import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "paper_source.py"
SPEC = importlib.util.spec_from_file_location("theory_first_paper_source", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
paper_source = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = paper_source
SPEC.loader.exec_module(paper_source)


class FakeResponse(io.BytesIO):
    def __init__(self, payload: bytes, url: str, headers: dict[str, str] | None = None) -> None:
        super().__init__(payload)
        self._url = url
        self.status = 200
        self.headers = headers or {
            "Content-Type": "application/pdf",
            "Content-Length": str(len(payload)),
            "Content-Encoding": "identity",
        }

    def geturl(self) -> str:
        return self._url

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class FakeOpener:
    def __init__(self, payload: bytes, url: str) -> None:
        self.payload = payload
        self.url = url
        self.calls = 0

    def open(self, request: object, timeout: float) -> FakeResponse:
        self.calls += 1
        self.timeout = timeout
        return FakeResponse(self.payload, self.url)


class ArxivValidationTests(unittest.TestCase):
    def test_accepts_modern_and_old_identifiers(self) -> None:
        accepted = (
            "1706.03762",
            "1706.03762v2",
            "hep-th/9901001",
            "math.GT/0309136v1",
        )
        for identifier in accepted:
            with self.subTest(identifier=identifier):
                self.assertEqual(paper_source.normalize_arxiv_id(identifier), identifier)

    def test_rejects_urls_traversal_and_malformed_identifiers(self) -> None:
        rejected = (
            "https://arxiv.org/pdf/1706.03762",
            "../1706.03762",
            "hep-th/../../etc/passwd",
            "2412.1",
            "arXiv:1706.03762",
            "file:///tmp/paper.pdf",
        )
        for identifier in rejected:
            with self.subTest(identifier=identifier):
                with self.assertRaises(paper_source.UserFacingError):
                    paper_source.normalize_arxiv_id(identifier)

    def test_redirect_validation_is_same_host_https_and_exact_path(self) -> None:
        identifier = "hep-th/9901001"
        paper_source.validate_arxiv_pdf_url(
            "https://arxiv.org/pdf/hep-th/9901001.pdf", identifier
        )
        rejected = (
            "http://arxiv.org/pdf/hep-th/9901001",
            "https://example.org/pdf/hep-th/9901001",
            "https://arxiv.org@127.0.0.1/pdf/hep-th/9901001",
            "https://arxiv.org/pdf/hep-th/9901001?download=1",
            "https://arxiv.org/abs/hep-th/9901001",
        )
        for url in rejected:
            with self.subTest(url=url):
                with self.assertRaises(paper_source.UserFacingError):
                    paper_source.validate_arxiv_pdf_url(url, identifier)

    def test_dns_guard_rejects_any_non_public_answer(self) -> None:
        public = [(2, 1, 6, "", ("8.8.8.8", 443))]
        with mock.patch.object(paper_source.socket, "getaddrinfo", return_value=public):
            paper_source.ensure_public_arxiv_resolution()

        mixed = public + [(2, 1, 6, "", ("127.0.0.1", 443))]
        with mock.patch.object(paper_source.socket, "getaddrinfo", return_value=mixed):
            with self.assertRaises(paper_source.UserFacingError) as context:
                paper_source.ensure_public_arxiv_resolution()
        self.assertEqual(context.exception.code, "unsafe_resolution")


class CacheAndDownloadTests(unittest.TestCase):
    def test_offline_download_is_atomic_private_and_cacheable(self) -> None:
        identifier = "1706.03762"
        payload = b"%PDF-1.4\n% bounded offline fixture\n%%EOF\n"
        with tempfile.TemporaryDirectory() as temporary:
            cache = Path(temporary) / "cache"
            opener = FakeOpener(payload, paper_source.build_arxiv_pdf_url(identifier))
            path, hit, size, digest = paper_source._download_arxiv_pdf(
                identifier,
                cache,
                max_bytes=4096,
                timeout_seconds=5,
                opener=opener,
                resolve_host=False,
            )
            self.assertFalse(hit)
            self.assertEqual(path.read_bytes(), payload)
            self.assertEqual(size, len(payload))
            self.assertEqual(len(digest), 64)
            self.assertEqual(path.stat().st_mode & 0o077, 0)
            self.assertFalse(any(path.parent.glob("*.part")))

            second, hit, _, _ = paper_source._download_arxiv_pdf(
                identifier,
                cache,
                max_bytes=4096,
                timeout_seconds=5,
                opener=opener,
                resolve_host=False,
            )
            self.assertTrue(hit)
            self.assertEqual(second, path)
            self.assertEqual(opener.calls, 1)

    def test_cleanup_refuses_foreign_entries_and_missing_roots(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            missing = Path(temporary) / "missing"
            with self.assertRaises(paper_source.UserFacingError):
                paper_source.clean_managed_cache(missing)
            self.assertFalse(missing.exists())

            root = Path(temporary) / "cache"
            papers = paper_source.ensure_managed_cache(root)
            foreign = root / "keep-me.txt"
            foreign.write_text("not managed", encoding="utf-8")
            with self.assertRaises(paper_source.UserFacingError) as context:
                paper_source.clean_managed_cache(root)
            self.assertEqual(context.exception.code, "cleanup_refused")
            self.assertTrue(foreign.exists())

            foreign.unlink()
            foreign_paper = papers / "user-owned-paper.pdf"
            foreign_paper.write_bytes(b"%PDF-foreign")
            foreign_paper.chmod(0o600)
            with self.assertRaises(paper_source.UserFacingError) as context:
                paper_source.clean_managed_cache(root)
            self.assertEqual(context.exception.code, "cleanup_refused")
            self.assertTrue(foreign_paper.exists())

            foreign_paper.unlink()
            managed = papers / "1706.03762.pdf"
            managed.write_bytes(b"%PDF-test")
            managed.chmod(0o600)
            result = paper_source.clean_managed_cache(root)
            self.assertEqual(result["removed_files"], 1)
            self.assertFalse(root.exists())


@unittest.skipUnless(importlib.util.find_spec("pypdf") is not None, "pypdf is not installed")
class ExtractionTests(unittest.TestCase):
    @staticmethod
    def _make_pdf(path: Path, pages: int = 1) -> None:
        from pypdf import PdfWriter
        from pypdf.generic import DictionaryObject, NameObject, StreamObject

        document = PdfWriter()
        for index in range(pages):
            page = document.add_blank_page(width=612, height=792)
            font = DictionaryObject(
                {
                    NameObject("/Type"): NameObject("/Font"),
                    NameObject("/Subtype"): NameObject("/Type1"),
                    NameObject("/BaseFont"): NameObject("/Helvetica"),
                }
            )
            font_reference = document._add_object(font)
            page[NameObject("/Resources")] = DictionaryObject(
                {NameObject("/Font"): DictionaryObject({NameObject("/F1"): font_reference})}
            )
            content = StreamObject()
            content.set_data(
                f"BT /F1 12 Tf 72 720 Td (Untrusted source text page {index + 1}) Tj ET".encode()
            )
            page[NameObject("/Contents")] = document._add_object(content)
        with path.open("wb") as handle:
            document.write(handle)

    def test_extracts_in_worker_without_preview_or_path_leak(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "private-hypothesis-name.pdf"
            output = root / "out"
            self._make_pdf(source)
            result = paper_source.extract_pdf_isolated(
                source,
                output,
                max_bytes=1024 * 1024,
                max_pages=5,
                max_text_bytes=1024 * 1024,
                timeout_seconds=20,
                max_memory_mib=1024,
            )
            serialized = json.dumps(result)
            self.assertNotIn(str(root), serialized)
            self.assertNotIn(source.name, serialized)
            self.assertIsNone(result["text_preview"])
            self.assertIn("Untrusted source text", (output / "paper.txt").read_text())

            metadata = json.loads((output / "metadata.json").read_text())
            self.assertNotIn(str(root), json.dumps(metadata))
            self.assertNotIn(source.name, json.dumps(metadata))
            self.assertTrue(metadata["complete"])
            self.assertEqual((output / "paper.txt").stat().st_mode & 0o077, 0)

    def test_page_limit_fails_closed_without_publishing_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "two-pages.pdf"
            output = root / "out"
            self._make_pdf(source, pages=2)
            with self.assertRaises(paper_source.UserFacingError) as context:
                paper_source.extract_pdf_isolated(
                    source,
                    output,
                    max_bytes=1024 * 1024,
                    max_pages=1,
                    max_text_bytes=1024 * 1024,
                    timeout_seconds=20,
                    max_memory_mib=1024,
                )
            self.assertEqual(context.exception.code, "page_limit")
            self.assertFalse((output / "paper.txt").exists())
            self.assertFalse((output / "metadata.json").exists())

    def test_cli_redacts_paths_and_source_text(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "sensitive-paper-name.pdf"
            output = root / "out"
            self._make_pdf(source)
            process = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "extract",
                    "--pdf",
                    str(source),
                    "--output-dir",
                    str(output),
                    "--parse-timeout-seconds",
                    "20",
                ],
                check=False,
                capture_output=True,
                text=True,
                shell=False,
                timeout=30,
                env=os.environ.copy(),
            )
            self.assertEqual(process.returncode, 0, process.stderr)
            combined = process.stdout + process.stderr
            self.assertNotIn(str(root), combined)
            self.assertNotIn(source.name, combined)
            self.assertNotIn("Untrusted source text", combined)
            payload = json.loads(process.stdout)
            self.assertIsNone(payload["text_preview"])


if __name__ == "__main__":
    unittest.main()
