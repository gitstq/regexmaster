"""
Utility functions for RegexMaster.
"""

import re
from typing import Optional


def escape_regex(pattern: str) -> str:
    """
    Escape special regex characters in a string.

    Args:
        pattern: String to escape

    Returns:
        Escaped string safe for regex use
    """
    return re.escape(pattern)


def unescape_regex(pattern: str) -> str:
    """
    Remove escape characters from a regex pattern.

    Args:
        pattern: Escaped pattern

    Returns:
        Unescaped string
    """
    # Remove backslashes before special characters
    return re.sub(r"\\([^\w])", r"\1", pattern)


def validate_pattern(pattern: str) -> tuple[bool, Optional[str]]:
    """
    Validate a regex pattern.

    Args:
        pattern: Pattern to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        re.compile(pattern)
        return True, None
    except re.error as e:
        return False, str(e)


def count_groups(pattern: str) -> int:
    """
    Count the number of capturing groups in a pattern.

    Args:
        pattern: Regex pattern

    Returns:
        Number of capturing groups
    """
    try:
        compiled = re.compile(pattern)
        return compiled.groups
    except re.error:
        return 0


def get_group_names(pattern: str) -> list[str]:
    """
    Get the names of named groups in a pattern.

    Args:
        pattern: Regex pattern

    Returns:
        List of group names
    """
    try:
        compiled = re.compile(pattern)
        return list(compiled.groupindex.keys())
    except re.error:
        return []


def format_match(match: re.Match, show_groups: bool = True) -> str:
    """
    Format a match object for display.

    Args:
        match: Match object
        show_groups: Whether to show group information

    Returns:
        Formatted string
    """
    lines = [f"Match: '{match.group()}'"]
    lines.append(f"  Position: {match.start()}-{match.end()}")

    if show_groups and match.groups():
        lines.append("  Groups:")
        for i, group in enumerate(match.groups(), 1):
            lines.append(f"    {i}: '{group}'")

        if match.groupdict():
            lines.append("  Named Groups:")
            for name, value in match.groupdict().items():
                lines.append(f"    {name}: '{value}'")

    return "\n".join(lines)


def highlight_matches(text: str, matches: list[re.Match]) -> str:
    """
    Highlight matches in text using ANSI codes.

    Args:
        text: Original text
        matches: List of match objects

    Returns:
        Text with highlighted matches
    """
    if not matches:
        return text

    # Build a list of (start, end, is_match) tuples
    positions = []
    for match in matches:
        positions.append((match.start(), match.end(), True))

    # Sort by position
    positions.sort()

    # Build highlighted string
    result = []
    last_end = 0

    for start, end, is_match in positions:
        # Add non-matching part
        if start > last_end:
            result.append(text[last_end:start])

        # Add matching part with highlight
        if is_match:
            result.append(f"\033[93m{text[start:end]}\033[0m")

        last_end = end

    # Add remaining text
    if last_end < len(text):
        result.append(text[last_end:])

    return "".join(result)
