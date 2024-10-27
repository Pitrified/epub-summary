"""Utils for the epubber module."""

import re
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup, Tag
from loguru import logger as lg

VALID_CHAP_EXT = [".xhtml", ".xml", ".html"]


def find_chapter_files(zipped_file_paths: list[Path]) -> list[Path]:
    """Find text chapters in epub."""
    # check that we have some files
    if len(zipped_file_paths) == 0:
        lg.warning("No files to find from.")
        return []

    # get the paths that are valid xhtml and similar
    chap_file_paths = [f for f in zipped_file_paths if f.suffix in VALID_CHAP_EXT]

    # stem gets the file name without extensions
    stems = [f.stem for f in chap_file_paths]

    # get the longest stem
    max_stem_len = max(len(c) for c in stems)

    # track the best regex' performances
    best_match_num = 0
    best_stem_re = re.compile("")

    # iterate over the len, looking for the best match
    for num_kept_chars in range(max_stem_len):

        # keep only the beginning of the names
        stem_chops = [s[:num_kept_chars] for s in stems]

        # count how many names have common prefix
        stem_freqs = Counter(stem_chops)

        # if there are no chapters with common prefix skip
        if stem_freqs.most_common()[0][1] == 1:
            continue

        # try to match the prefix with re
        for stem_might, stem_freq in stem_freqs.items():

            # compile a regex looking for name{number}
            stem_re = re.compile(f"{stem_might}(\\d+)")

            # how many matches this stem has
            good_match_num = 0

            # track if a regex fails: it can have some matches and then fail
            failed = False

            for stem in stems:
                stem_ch = stem[:num_kept_chars]
                match = stem_re.match(stem)

                # if the regex does not match but the stem prefix does, fails
                if match is None and stem_ch == stem_might:
                    failed = True
                    break

                good_match_num += 1

            # if this stem failed to match, don't consider it for the best
            if failed:
                continue

            # update info on best matching regex
            if good_match_num > best_match_num:
                best_stem_re = stem_re
                best_match_num = good_match_num

    # if the best match sucks keep all chapters
    if best_match_num <= 2:
        return chap_file_paths

    # pair chapter name and chapter number by using the best regex
    chap_file_paths_id: list[tuple[Path, int]] = []
    for stem, chap_file_path in zip(stems, chap_file_paths):
        # match the stem and get the chapter number
        match = best_stem_re.match(stem)
        if match is None:
            continue
        chap_id = int(match.group(1))
        chap_file_paths_id.append((chap_file_path, chap_id))

    # sort the list according to the extracted id
    chap_file_paths = [cid[0] for cid in sorted(chap_file_paths_id, key=lambda x: x[1])]
    return chap_file_paths


def tag_to_str(tag: Tag) -> str:
    """Convert a tag to a string."""
    tag_str = tag.text
    tag_str = tag_str.replace("\n\r", " ")
    tag_str = tag_str.replace("\n", " ")
    tag_str = tag_str.replace("\r", " ")
    return tag_str


def str_to_p_tag(tag_str: str) -> Tag:
    p_html = f"<p>{tag_str}</p>"
    p_tag = BeautifulSoup(p_html, features="lxml").p
    if p_tag is None:
        raise ValueError(f"Failed to convert {tag_str} to tag.")
    return p_tag
