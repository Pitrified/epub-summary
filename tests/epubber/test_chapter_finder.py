"""Test the chapter finder utility."""

from pathlib import Path

import pytest

from epub_summary.epubber.utils import find_chapter_files


def test_fcf_base() -> None:
    """The function can find chapter files."""
    zfp = [
        Path("chapter1.xhtml"),
        Path("chapter2.xhtml"),
        Path("chapter3.xhtml"),
        Path("chapter4.xhtml"),
    ]
    cfp = find_chapter_files(zfp)
    assert cfp == zfp


def test_fcf_chapter_sorting() -> None:
    """The function can sort chapter files by their numbers."""
    zfp = [
        Path("chapter1.xhtml"),
        Path("chapter11.xhtml"),
        Path("chapter12.xhtml"),
        Path("chapter3.xhtml"),
        Path("chapter2.xhtml"),
        Path("chapter4.xhtml"),
    ]
    cfp = find_chapter_files(zfp)
    expected = [
        Path("chapter1.xhtml"),
        Path("chapter2.xhtml"),
        Path("chapter3.xhtml"),
        Path("chapter4.xhtml"),
        Path("chapter11.xhtml"),
        Path("chapter12.xhtml"),
    ]
    assert cfp == expected


def test_identify_numbers_of_different_lengths() -> None:
    """The function can identify numbers of different lengths."""
    zfp = [
        Path("chapter1.xhtml"),
        Path("chapter2.xhtml"),
        Path("chapter3.xhtml"),
        Path("chapter40.xhtml"),
        Path("chapter50.xhtml"),
        Path("chapter60.xhtml"),
    ]
    cfp = find_chapter_files(zfp)
    assert cfp == zfp


def test_fcf_filter_other_chap() -> None:
    """The function can filter out non-chapter files."""
    zfp = [
        Path("intro.xhtml"),
        Path("chapter1.xhtml"),
        Path("chapter2.xhtml"),
        Path("chapter3.xhtml"),
        Path("chapter40.xhtml"),
        Path("chapter50.xhtml"),
        Path("chapter60.xhtml"),
        Path("not_a_chapter.xhtml"),
    ]
    cfp = find_chapter_files(zfp)
    assert cfp == zfp[1:-1]


def test_fcf_no_chapters() -> None:
    """The function can handle no chapters matching the regex."""
    zfp = [
        Path("intro.xhtml"),
        Path("not_a_chapter.xhtml"),
    ]
    cfp = find_chapter_files(zfp)
    assert cfp == zfp


def test_fcf_no_files() -> None:
    """The function can handle no files."""
    zfp = []
    cfp = find_chapter_files(zfp)
    assert cfp == zfp


def test_fcf_same_stem() -> None:
    """The function can handle chapters with the same stem."""
    zfp = [
        Path("chapter1.xhtml"),
        Path("chapter1.xhtml"),
        Path("chapter1.xhtml"),
        Path("chapter1.xhtml"),
    ]
    cfp = find_chapter_files(zfp)
    assert cfp == zfp


def test_fcf_same_stem_diff_numbers() -> None:
    """The function can handle chapters with the same stem but different numbers."""
    zfp = [
        Path("chapter.xhtml"),
        Path("chapter1.xhtml"),
        Path("chapter2.xhtml"),
        Path("chapter3.xhtml"),
    ]
    cfp = find_chapter_files(zfp)
    assert cfp == zfp
