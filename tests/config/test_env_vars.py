"""Test that the environment variables are available."""

import os

import pytest


def test_env_vars() -> None:
    """The environment var EPUB_SUMMARY_SAMPLE_ENV_VAR is available."""
    assert "EPUB_SUMMARY_SAMPLE_ENV_VAR" in os.environ
    assert os.environ["EPUB_SUMMARY_SAMPLE_ENV_VAR"] == "sample"
