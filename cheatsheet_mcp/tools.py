"""Tool implementations for the Python Cheatsheet MCP server."""

import re
from typing import List

from .parser import CheatsheetParser
from .utils import clean_markdown, format_section_summary, truncate

_parser = CheatsheetParser()


def search_python_concept(query: str) -> str:
    """Search for a Python concept or keyword in the cheatsheet.

    Args:
        query: The concept or keyword to search for (e.g. "list", "decorator", "async").

    Returns:
        Matching sections with summaries, or a not-found message.
    """
    results = _parser.search(query)
    if not results:
        return f"No sections found matching '{query}'. Try `list_topics` to see available topics."

    lines = [f"Found {len(results)} section(s) matching '{query}':\n"]
    for section in results[:5]:
        lines.append(format_section_summary(section.title, section.content, section.code_blocks))
        lines.append("\n---\n")
    return truncate('\n'.join(lines))


def get_code_example(topic: str) -> str:
    """Get Python code examples for a specific topic.

    Args:
        topic: The topic to retrieve examples for (e.g. "list", "class", "generator").

    Returns:
        Code examples for the topic, or a not-found message.
    """
    section = _parser.find_section(topic)
    if not section:
        topics = _parser.get_topics()
        close = [t for t in topics if topic.lower() in t.lower()]
        if close:
            return (
                f"No exact section found for '{topic}'. "
                f"Did you mean one of: {', '.join(close[:5])}? "
                "Use the exact topic name."
            )
        return f"No section found for '{topic}'. Use `list_topics` to see all topics."

    if not section.code_blocks:
        return f"Section '{section.title}' has no code examples."

    lines = [f"## {section.title} — Code Examples\n"]
    for i, block in enumerate(section.code_blocks, 1):
        lines.append(f"**Example {i}:**")
        lines.append("```python")
        lines.append(block)
        lines.append("```\n")
    return truncate('\n'.join(lines), max_length=4000)


def explain_concept(concept: str) -> str:
    """Get a detailed explanation of a Python concept.

    Args:
        concept: The concept to explain (e.g. "generator", "decorator", "class").

    Returns:
        A detailed explanation including description, usage, and code examples.
    """
    section = _parser.find_section(concept)
    if not section:
        return (
            f"No explanation found for '{concept}'. "
            "Try `search_python_concept` to find related sections."
        )

    plain = clean_markdown(section.content)
    lines = [f"## {section.title}\n", plain, ""]
    if section.code_blocks:
        lines.append("### Code Examples\n")
        for i, block in enumerate(section.code_blocks[:3], 1):
            lines.append(f"**Example {i}:**")
            lines.append("```python")
            lines.append(block)
            lines.append("```\n")
    return truncate('\n'.join(lines), max_length=4000)


def search_best_practices(topic: str) -> str:
    """Search for Python best practices related to a topic.

    Args:
        topic: The topic to look up best practices for (e.g. "error handling", "class design").

    Returns:
        Best practice notes and patterns extracted from the cheatsheet.
    """
    results = _parser.search(topic)
    if not results:
        return (
            f"No best practices found for '{topic}'. "
            "Try a broader term or use `list_topics`."
        )

    # Look for bullet-point / note lines which typically contain best practices
    practice_pattern = re.compile(
        r'^\s*[\*\-]\s+\*\*.*?\*\*.*$|^\s*[\*\-]\s+.*(?:should|avoid|prefer|use|never|always).*$',
        re.IGNORECASE | re.MULTILINE,
    )

    lines = [f"### Best Practices related to '{topic}':\n"]
    found_any = False
    for section in results[:5]:
        practices = practice_pattern.findall(section.content)
        if practices:
            found_any = True
            lines.append(f"**{section.title}:**")
            for p in practices[:5]:
                lines.append(clean_markdown(p.strip()))
            lines.append("")

    if not found_any:
        # Fall back to a summary of first result
        s = results[0]
        lines.append(format_section_summary(s.title, s.content, s.code_blocks))

    return truncate('\n'.join(lines))


def list_topics() -> str:
    """List all available topics in the Python cheatsheet.

    Returns:
        A formatted list of all topic headings available in the cheatsheet.
    """
    topics = _parser.get_topics()
    if not topics:
        return "No topics found."
    lines = ["## Python Cheatsheet Topics\n"]
    for topic in topics:
        lines.append(f"- {topic}")
    lines.append(
        "\nUse `get_code_example`, `explain_concept`, or `search_python_concept` "
        "with any of these topic names."
    )
    return '\n'.join(lines)
