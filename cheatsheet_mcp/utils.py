"""Utility functions for the Python Cheatsheet MCP server."""

import re


def clean_markdown(text: str) -> str:
    """Strip markdown syntax to produce plain text."""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove bold/italic markers
    text = re.sub(r'\*{1,3}([^*]+)\*{1,3}', r'\1', text)
    text = re.sub(r'_{1,3}([^_]+)_{1,3}', r'\1', text)
    # Remove inline code
    text = re.sub(r'`([^`]+)`', r'\1', text)
    # Remove links but keep text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove HTML entities
    text = re.sub(r'&\w+;', ' ', text)
    # Collapse whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def truncate(text: str, max_length: int = 2000) -> str:
    """Truncate text to max_length characters, adding ellipsis if needed."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + '...'


def format_section_summary(title: str, content: str, code_blocks: list) -> str:
    """Format a section into a concise summary string."""
    summary_lines = [f"## {title}", ""]
    plain = clean_markdown(content)
    # Take first paragraph as description
    paragraphs = [p.strip() for p in plain.split('\n\n') if p.strip()]
    if paragraphs:
        summary_lines.append(paragraphs[0])
        summary_lines.append("")
    if code_blocks:
        summary_lines.append("**Example:**")
        summary_lines.append("```python")
        summary_lines.append(code_blocks[0])
        summary_lines.append("```")
    return '\n'.join(summary_lines)
