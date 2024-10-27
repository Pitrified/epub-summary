"""Epub."""

from pathlib import Path
from typing import Self
import zipfile

from bs4 import BeautifulSoup, Tag
from loguru import logger as lg

from epub_summary.epubber.utils import find_chapter_files, str_to_p_tag, tag_to_str


class EpubParagraph:
    """EpubParagraph."""

    def __init__(self) -> None:
        """Initialize epub paragraph."""

    def set_p_tag(self, p_tag: Tag) -> None:
        """Set the p tag of the paragraph."""
        self.p_tag = p_tag
        self.set_p_str(tag_to_str(self.p_tag))

    def set_p_str(self, p_str: str) -> None:
        """Set the p string of the paragraph."""
        self.p_str = p_str
        self.p_tag = str_to_p_tag(self.p_str)

    @classmethod
    def from_p_str(cls, p_str: str) -> Self:
        """Create a paragraph from a string."""
        par = cls()
        par.set_p_str(p_str)
        return par

    @classmethod
    def from_p_tag(cls, p_tag: Tag) -> Self:
        """Create a paragraph from a tag."""
        par = cls()
        par.set_p_tag(p_tag)
        return par


class EpubChapter:
    """EpubChapter."""

    def __init__(self) -> None:
        """Initialize epub chapter."""
        self.html: str = ""
        self.paragraphs: list[EpubParagraph] = []

    @property
    def text(self) -> str:
        """Get the text of the chapter."""
        return "\n".join([p.p_str for p in self.paragraphs])

    @text.setter
    def text(self, text: str) -> None:
        """Set the text of the chapter."""
        pars = text.split("\n")
        pars_html = [f"<p>{p}</p>" for p in pars]
        pars_html_one = "\n".join(pars_html)
        text_html = f"<body>{pars_html_one}</body>"
        self.set_html(text_html)

    def set_html(self, html: str) -> None:
        """Set the html of the chapter."""
        self.html = html
        self.update_soup()

    def set_chap_stem(self, chap_stem: str) -> None:
        """Set the chapter stem."""
        self.chap_stem = chap_stem

    def add_paragraph(self, paragraph: EpubParagraph) -> None:
        """Add a paragraph to the chapter."""
        self.paragraphs.append(paragraph)

    def update_soup(self) -> None:
        """Update the soup of the chapter."""
        # parse the soup and get the body
        # TODO filter XMLParsedAsHTMLWarning
        self.soup = BeautifulSoup(markup=self.html, features="lxml")
        self.body = self.soup.body
        if self.body is None:
            lg.warning(f"No body found in chapter {self.chap_stem}.")
            return
        # find the paragraphs
        self.all_p_tag = self.body.find_all("p")
        if len(self.all_p_tag) == 0:
            lg.warning(f"No paragraphs found in chapter {self.chap_stem}.")
            return
        # build the list of Paragraphs
        for p_tag in self.all_p_tag:
            par = EpubParagraph.from_p_tag(p_tag)
            self.add_paragraph(par)

    @classmethod
    def from_html(cls, html: str, chap_stem: str) -> Self:
        """Create a chapter from html."""
        chapter = cls()
        chapter.set_chap_stem(chap_stem)
        chapter.set_html(html)
        return chapter


class Epub:
    """Epub."""

    def __init__(self) -> None:
        """Initialize epub loader."""
        # self.epub_fp: Path | None = None
        self.chapters: list[EpubChapter] = []

    def set_epub_fp(self, epub_fp: Path) -> None:
        """Set the epub file path."""
        self.epub_fp = epub_fp

    def load_zip(self, epub_fp: Path) -> None:
        """Load epub from zip file."""
        # set the epub file path
        self.set_epub_fp(epub_fp)
        # load the zip (epub) file in memory
        input_zip = zipfile.ZipFile(self.epub_fp)
        # get the paths of the files in the zip
        input_zip_fps = [Path(p) for p in input_zip.namelist()]
        # find the files with the chapters
        chapter_fps = find_chapter_files(input_zip_fps)
        for chapter_fp in chapter_fps:
            # read the chapter file and decode it
            chapter_bytes = input_zip.read(str(chapter_fp))
            chapter_html = chapter_bytes.decode("utf-8")
            # create a chapter object
            chapter = EpubChapter.from_html(chapter_html, chapter_fp.stem)
            # add the chapter to the epub
            self.add_chapter(chapter)

    def add_chapter(self, chapter: EpubChapter) -> None:
        """Add a chapter to the epub."""
        self.chapters.append(chapter)

    @classmethod
    def from_zip(cls, epub_fp: Path) -> Self:
        """Load epub from zip file."""
        ep = cls()
        ep.load_zip(epub_fp)
        return ep
