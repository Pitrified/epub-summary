"""Epub."""

from abc import ABC
from pathlib import Path
from typing import Self
import zipfile

from bs4 import BeautifulSoup, Tag
from loguru import logger as lg

from epub_summary.epubber.utils import find_chapter_files, str_to_p_tag, tag_to_str


class BaseHtmlChapterParser(ABC):
    """ABC for HtmlChapterParser."""

    @staticmethod
    def parse(html: str) -> "list[EpubParagraph]":
        """Parse the html."""
        raise NotImplementedError


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


class EpubSection:
    """EpubSection."""

    def __init__(self, section_title: str) -> None:
        """Initialize epub section."""
        self.section_title = section_title
        self.paragraphs: list[EpubParagraph] = []

    def add_paragraph(self, paragraph: EpubParagraph) -> None:
        """Add a paragraph to the section."""
        self.paragraphs.append(paragraph)

    @property
    def text(self) -> str:
        """Get the text of the section."""
        return "\n".join([p.p_str for p in self.paragraphs])


class EpubChapter:
    """EpubChapter."""

    def __init__(self) -> None:
        """Initialize epub chapter."""
        self.html: str = ""
        self.sections: list[EpubSection] = []

    @property
    def text(self) -> str:
        """Get the text of the chapter."""
        return "\n".join([s.text for s in self.sections])

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

    # def add_paragraph(self, section_title: str, paragraph: EpubParagraph) -> None:
    #     """Add a paragraph to the chapter."""
    #     # TODO improve, what if the section does not exist?
    #     section_titles = [s.section_title for s in self.sections]
    #     section_idx = section_titles.index(section_title)
    #     self.sections[section_idx].add_paragraph(paragraph)

    def add_section(self, section: EpubSection) -> None:
        """Add a section to the chapter."""
        self.sections.append(section)

    def update_soup(self) -> None:
        """Update the soup of the chapter."""
        # parse the soup and get the body
        # TODO filter XMLParsedAsHTMLWarning
        # TODO add a custom extractor from html to paragraphs
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
        sec = EpubSection("default")
        for p_tag in self.all_p_tag:
            par = EpubParagraph.from_p_tag(p_tag)
            sec.add_paragraph(par)
        self.add_section(sec)

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
