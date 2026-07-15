from __future__ import annotations

import importlib.util
import json
import stat
from pathlib import Path
from types import ModuleType

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "plugins"
    / "theory-first"
    / "skills"
    / "deep-read-paper"
    / "scripts"
    / "paper_source.py"
)


def _load_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("theory_first_paper_source", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


paper_source = _load_module()


@pytest.mark.parametrize(
    "identifier",
    ["1706.03762", "1706.03762v2", "hep-th/9901001", "math.GT/0309136v1"],
)
def test_recognizes_modern_and_old_arxiv_ids(identifier: str) -> None:
    assert paper_source.normalize_arxiv_id(identifier) == identifier
    assert paper_source.build_arxiv_pdf_url(identifier).startswith(
        "https://arxiv.org/pdf/"
    )


@pytest.mark.parametrize(
    "identifier",
    [
        "https://arxiv.org/pdf/1706.03762",
        "../../etc/passwd",
        "1706.03762?download=1",
        "1706.03762;touch-pwned",
        "hep-th/../../etc/passwd",
        "",
    ],
)
def test_rejects_non_identifier_input(identifier: str) -> None:
    with pytest.raises(paper_source.UserFacingError) as caught:
        paper_source.normalize_arxiv_id(identifier)
    assert caught.value.code == "invalid_arxiv_id"


@pytest.mark.parametrize(
    "url",
    [
        "http://arxiv.org/pdf/1706.03762",
        "https://example.org/pdf/1706.03762",
        "https://arxiv.org.evil.test/pdf/1706.03762",
        "https://arxiv.org/pdf/1706.03762?next=https://127.0.0.1/",
        "https://user@arxiv.org/pdf/1706.03762",
        "https://arxiv.org:444/pdf/1706.03762",
        "https://arxiv.org/abs/1706.03762",
    ],
)
def test_rejects_unsafe_redirects(url: str) -> None:
    with pytest.raises(paper_source.UserFacingError) as caught:
        paper_source.validate_arxiv_pdf_url(url, "1706.03762")
    assert caught.value.code == "unsafe_redirect"


class _FakeResponse:
    status = 200

    def __init__(self, payload: bytes, url: str) -> None:
        self._payload = payload
        self._offset = 0
        self._url = url
        self.headers = {
            "Content-Length": str(len(payload)),
            "Content-Encoding": "identity",
        }

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def geturl(self) -> str:
        return self._url

    def read(self, size: int) -> bytes:
        block = self._payload[self._offset : self._offset + size]
        self._offset += len(block)
        return block


class _FakeOpener:
    def __init__(self, payload: bytes, url: str) -> None:
        self.payload = payload
        self.url = url
        self.calls = 0

    def open(self, request: object, timeout: float) -> _FakeResponse:
        assert timeout > 0
        self.calls += 1
        return _FakeResponse(self.payload, self.url)


def test_download_is_atomic_private_and_path_redacted(tmp_path: Path) -> None:
    cache = tmp_path / "private-cache"
    payload = b"%PDF-1.4\n" + (b"x" * 1100)
    url = "https://arxiv.org/pdf/1706.03762"
    opener = _FakeOpener(payload, url)

    artifact, cache_hit, size, digest = paper_source._download_arxiv_pdf(
        "1706.03762",
        cache,
        max_bytes=2048,
        timeout_seconds=5,
        opener=opener,
        resolve_host=False,
    )

    assert cache_hit is False
    assert opener.calls == 1
    assert size == len(payload)
    assert len(digest) == 64
    assert stat.S_IMODE(cache.stat().st_mode) == 0o700
    assert stat.S_IMODE(artifact.stat().st_mode) == 0o600
    assert list(artifact.parent.glob("*.part")) == []

    result = {
        "cache_ref": paper_source._path_ref(cache),
        "relative_artifact": f"papers/{artifact.name}",
    }
    rendered = json.dumps(result)
    assert str(tmp_path) not in rendered

    second = _FakeOpener(b"not used", url)
    cached_artifact, cache_hit, _, _ = paper_source._download_arxiv_pdf(
        "1706.03762",
        cache,
        max_bytes=2048,
        timeout_seconds=5,
        opener=second,
        resolve_host=False,
    )
    assert cached_artifact == artifact
    assert cache_hit is True
    assert second.calls == 0


def test_cleanup_refuses_foreign_files(tmp_path: Path) -> None:
    cache = tmp_path / "private-cache"
    papers = paper_source.ensure_managed_cache(cache)
    foreign = papers / "my-paper.pdf"
    foreign.write_bytes(b"%PDF-foreign")
    foreign.chmod(0o600)

    with pytest.raises(paper_source.UserFacingError) as caught:
        paper_source.clean_managed_cache(cache)
    assert caught.value.code == "cleanup_refused"
    assert foreign.exists()


def test_staging_rejects_a_source_changed_after_validation(tmp_path: Path) -> None:
    source = tmp_path / "source.pdf"
    source.write_bytes(b"%PDF-1.4\n" + (b"a" * 1100))
    size, digest = paper_source.validate_pdf(source, 2048)
    source.write_bytes(b"%PDF-1.4\n" + (b"b" * 1100))

    staging = tmp_path / "staging"
    with pytest.raises(paper_source.UserFacingError) as caught:
        paper_source._stage_verified_pdf(
            source,
            staging,
            expected_size=size,
            expected_digest=digest,
            max_bytes=2048,
        )
    assert caught.value.code == "source_changed"
    assert not (staging / "source.pdf").exists()


def test_replace_cannot_overwrite_the_source_pdf(tmp_path: Path) -> None:
    output = tmp_path / "output"
    output.mkdir(mode=0o700)
    source = output / "paper.txt"
    original = b"%PDF-1.4\n" + (b"source" * 200)
    source.write_bytes(original)

    with pytest.raises(paper_source.UserFacingError) as caught:
        paper_source.extract_pdf_isolated(
            source,
            output,
            max_bytes=4096,
            replace=True,
        )
    assert caught.value.code == "output_conflicts_source"
    assert source.read_bytes() == original


def test_extracts_without_returning_text_or_absolute_paths(tmp_path: Path) -> None:
    pytest.importorskip("pypdf")
    from pypdf import PdfWriter
    from pypdf.generic import DictionaryObject, NameObject, StreamObject

    source = tmp_path / "source.pdf"
    document = PdfWriter()
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
    content.set_data(b"BT /F1 12 Tf 72 720 Td (private navigation text) Tj ET")
    page[NameObject("/Contents")] = document._add_object(content)
    with source.open("wb") as handle:
        document.write(handle)

    output = tmp_path / "output"
    result = paper_source.extract_pdf_isolated(
        source,
        output,
        max_bytes=1024 * 1024,
        max_pages=2,
        max_text_bytes=64 * 1024,
        timeout_seconds=20,
        max_memory_mib=1024,
    )

    rendered = json.dumps(result)
    assert result["status"] == "ok"
    assert result["text_preview"] is None
    assert "private navigation text" not in rendered
    assert str(tmp_path) not in rendered
    assert stat.S_IMODE(output.stat().st_mode) == 0o700
    assert stat.S_IMODE((output / "paper.txt").stat().st_mode) == 0o600
    assert stat.S_IMODE((output / "metadata.json").stat().st_mode) == 0o600


def test_cli_error_does_not_echo_sensitive_paths(capsys: pytest.CaptureFixture[str]) -> None:
    sensitive = "/secret/researcher/private-paper.pdf"
    return_code = paper_source.main(
        ["extract", "--pdf", sensitive, "--output-dir", "/secret/output"]
    )
    captured = capsys.readouterr()
    assert return_code == 2
    assert sensitive not in captured.out + captured.err
    assert "/secret/output" not in captured.out + captured.err
