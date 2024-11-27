"""
Module to extract header tags from Azure Pipelines YAML files.
"""

import re
from typing import Dict, List

TAGS = ["@title", "@description", "@author", "@version"]


def extract_header_tags(file_path: str, tags: List[str] = TAGS) -> Dict[str, str]:
    """
    Extracts specified tags from the header comments of a file, handling global indentation.

    Parameters
    ----------
    file_path : str
        Path to the file containing the header comments.
    tags : List[str], optional
        List of tags to extract. Default includes common metadata tags.

    Returns
    -------
    Dict[str, str]
        A dictionary where keys are the tags and values are the corresponding extracted content.
    """
    tag_pattern = re.compile(
        r"^#\s*(" + "|".join(re.escape(tag) for tag in tags) + r"):\s*(.*)?"
    )
    indent_pattern = re.compile(r"^#\s+(.+)")  # Matches indented continuation lines

    extracted = {}
    current_tag = None

    with open(file_path, "r") as file:
        # Read all lines and normalize indentation
        lines = file.readlines()
        stripped_lines = [
            line.lstrip() for line in lines if line.strip().startswith("#")
        ]

        for line in stripped_lines:
            stripped = line.strip()

            # Match primary tags
            tag_match = tag_pattern.match(stripped)
            if tag_match:
                current_tag = tag_match.group(1)
                extracted[current_tag] = (
                    tag_match.group(2).strip() if tag_match.group(2) else ""
                )
                continue

            # Match continuation lines
            if current_tag and indent_pattern.match(stripped):
                extracted[current_tag] += " " + indent_pattern.match(stripped).group(1)

    return {key: value.strip() for key, value in extracted.items()}
