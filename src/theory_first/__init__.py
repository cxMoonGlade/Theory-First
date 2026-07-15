from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version


try:
    __version__ = version("theory-first")
except PackageNotFoundError:  # Source checkout without an installed distribution.
    __version__ = "0+unknown"


__all__ = ["__version__"]
