"""Parser for the Python Cheatsheet README.md file."""

import re
from pathlib import Path
from typing import Dict, List, Optional


class Section:
    """Represents a section of the Python cheatsheet."""

    def __init__(self, title: str, level: int, content: str, code_blocks: List[str]):
        self.title = title
        self.level = level
        self.content = content
        self.code_blocks = code_blocks

    def __repr__(self) -> str:
        return f"Section(title={self.title!r}, level={self.level}, code_blocks={len(self.code_blocks)})"


class CheatsheetParser:
    """Parses the Python Cheatsheet README.md into structured sections."""

    # Heading patterns: setext-style (underlined) and ATX-style (#)
    SETEXT_H1 = re.compile(r'^(.+)\n={3,}\s*$', re.MULTILINE)
    SETEXT_H2 = re.compile(r'^(.+)\n-{3,}\s*$', re.MULTILINE)
    ATX_HEADING = re.compile(r'^(#{1,6})\s+(.+)', re.MULTILINE)
    CODE_BLOCK = re.compile(r'```(?:python|bash|)?\n(.*?)```', re.DOTALL)

    def __init__(self, readme_path: Optional[Path] = None):
        if readme_path is None:
            readme_path = Path(__file__).parent.parent / 'README.md'
        self.readme_path = readme_path
        self._sections: Optional[List[Section]] = None

    def _load(self) -> str:
        with open(self.readme_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _extract_code_blocks(self, text: str) -> List[str]:
        return [m.group(1).strip() for m in self.CODE_BLOCK.finditer(text)]

    def parse(self) -> List[Section]:
        """Parse the README.md and return a list of Section objects."""
        if self._sections is not None:
            return self._sections

        content = self._load()

        # Split the document on setext-style headings (level 2 are the main topics)
        # We'll use a unified approach: find all headings and their positions
        heading_positions = []

        # Find setext H1
        for m in self.SETEXT_H1.finditer(content):
            heading_positions.append((m.start(), 1, m.group(1).strip(), m.end()))

        # Find setext H2
        for m in self.SETEXT_H2.finditer(content):
            # Make sure it's not an H1 already captured
            title = m.group(1).strip()
            if not any(abs(pos - m.start()) < 5 for pos, level, _, _ in heading_positions if level == 1):
                heading_positions.append((m.start(), 2, title, m.end()))

        # Find ATX headings
        for m in self.ATX_HEADING.finditer(content):
            level = len(m.group(1))
            title = m.group(2).strip()
            heading_positions.append((m.start(), level, title, m.end()))

        # Sort by position
        heading_positions.sort(key=lambda x: x[0])

        sections = []
        for i, (start, level, title, end) in enumerate(heading_positions):
            # Section content goes from end of heading to start of next heading
            next_start = heading_positions[i + 1][0] if i + 1 < len(heading_positions) else len(content)
            section_content = content[end:next_start].strip()
            code_blocks = self._extract_code_blocks(section_content)
            sections.append(Section(
                title=title,
                level=level,
                content=section_content,
                code_blocks=code_blocks,
            ))

        self._sections = sections
        return sections

    def get_topics(self) -> List[str]:
        """Return a list of all top-level topic names (level-2 headings)."""
        return [s.title for s in self.parse() if s.level == 2]

    def find_section(self, query: str) -> Optional[Section]:
        """Find a section by exact or partial title match (case-insensitive)."""
        query_lower = query.lower()
        sections = self.parse()
        # Exact match first
        for section in sections:
            if section.title.lower() == query_lower:
                return section
        # Partial match
        for section in sections:
            if query_lower in section.title.lower():
                return section
        return None

    def search(self, query: str) -> List[Section]:
        """Return all sections whose title or content contains the query string."""
        query_lower = query.lower()
        results = []
        for section in self.parse():
            if query_lower in section.title.lower() or query_lower in section.content.lower():
                results.append(section)
        return results
