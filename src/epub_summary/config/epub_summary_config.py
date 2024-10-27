"""EpubSummary project configuration."""

from loguru import logger as lg

from epub_summary.config.epub_summary_paths import EpubSummaryPaths
from epub_summary.config.singleton import Singleton


class EpubSummaryConfig(metaclass=Singleton):
    """EpubSummary project configuration."""

    def __init__(self) -> None:
        lg.info(f"Loading EpubSummary config")
        self.paths = EpubSummaryPaths()

    def __str__(self) -> str:
        s = "EpubSummaryConfig:"
        s += f"\n{self.paths}"
        return s

    def __repr__(self) -> str:
        return str(self)


EPUB_SUMMARY_CONFIG = EpubSummaryConfig()
EPUB_SUMMARY_PATHS = EPUB_SUMMARY_CONFIG.paths
