"""Test the epub_summary paths."""

import pytest

from epub_summary.config.epub_summary_config import EPUB_SUMMARY_PATHS


def test_epub_summary_paths() -> None:
    """Test the epub_summary paths."""
    assert EPUB_SUMMARY_PATHS.src_fol.name == "epub_summary"
    assert EPUB_SUMMARY_PATHS.root_fol.name == "epub_summary"
    assert EPUB_SUMMARY_PATHS.data_fol.name == "data"
