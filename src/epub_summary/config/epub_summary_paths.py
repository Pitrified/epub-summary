"""Paths and folders for data files."""

from pathlib import Path

from loguru import logger as lg

import epub_summary


class EpubSummaryPaths:
    """Paths and folders for data and resources."""

    def __init__(
        self,
    ) -> None:
        """Load the paths for the project."""
        self.load_paths()

    def load_paths(self) -> None:
        """Load the config for data folders."""
        self.load_repo_paths()
        self.load_external_paths()

    def load_repo_paths(self) -> None:
        """Pre load the common config."""
        # src folder of the package
        self.src_fol = Path(epub_summary.__file__).parent
        # root folder of the project repository
        self.root_fol = self.src_fol.parents[1]
        # cache
        self.cache_fol = self.root_fol / "cache"
        # data
        self.data_fol = self.root_fol / "data"
        # static
        self.static_fol = self.root_fol / "static"

    def load_external_paths(self) -> None:
        """Load external files."""
        self.sample_epub_fol = Path.home() / "repos/snippet/datasets/ebook"
        self.dump_epub_fol = Path.home() / "ephem/epub/dump"

    def __str__(self) -> str:
        s = f"EpubSummaryPaths:\n"
        s += f"   src_fol: {self.src_fol}\n"
        s += f"  root_fol: {self.root_fol}\n"
        s += f" cache_fol: {self.cache_fol}\n"
        s += f"  data_fol: {self.data_fol}\n"
        s += f"static_fol: {self.static_fol}\n"
        return s
