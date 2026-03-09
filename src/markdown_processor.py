"""Markdown processor for the Python Cheatsheet.

Provides helper functions to process and extract structured information
from the README.md content.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def load_readme(path: Optional[Path] = None) -> str:
    """Load README.md content from the repository root."""
    if path is None:
        path = Path(__file__).parent.parent / 'README.md'
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_sections(content: str) -> List[Tuple[str, str]]:
    """Extract (heading, body) pairs from markdown content.

    Handles both setext-style (underlined) and ATX-style (#) headings.
    Returns a list of (title, body_text) tuples in document order.
    """
    # Find all headings with their positions
    heading_re = re.compile(
        r'(?:^(.+)\n={3,}\s*$)|(?:^(.+)\n-{3,}\s*$)|(?:^(#{1,6})\s+(.+))',
        re.MULTILINE,
    )
    positions: List[Tuple[int, str, int]] = []  # (start, title, end)
    for m in heading_re.finditer(content):
        if m.group(1):
            title, level = m.group(1).strip(), 1
        elif m.group(2):
            title, level = m.group(2).strip(), 2
        else:
            title, level = m.group(4).strip(), len(m.group(3))
        positions.append((m.start(), title, m.end()))

    result = []
    for i, (start, title, end) in enumerate(positions):
        next_start = positions[i + 1][0] if i + 1 < len(positions) else len(content)
        body = content[end:next_start].strip()
        result.append((title, body))
    return result


def extract_code_blocks(markdown_text: str) -> List[str]:
    """Extract all fenced code block contents from a markdown string."""
    pattern = re.compile(r'```(?:\w+)?\n(.*?)```', re.DOTALL)
    return [m.group(1).strip() for m in pattern.finditer(markdown_text)]


def extract_topics(content: str) -> List[str]:
    """Return all level-2 (setext-style dash-underlined) heading titles."""
    pattern = re.compile(r'^(.+)\n-{3,}\s*$', re.MULTILINE)
    return [m.group(1).strip() for m in pattern.finditer(content)]


def build_index(content: str) -> Dict[str, Dict]:
    """Build a search index mapping topic names to their section data.

    Returns a dict of {title: {"content": str, "code_blocks": List[str]}}.
    """
    sections = extract_sections(content)
    index: Dict[str, Dict] = {}
    for title, body in sections:
        index[title.lower()] = {
            "title": title,
            "content": body,
            "code_blocks": extract_code_blocks(body),
        }
    return index
