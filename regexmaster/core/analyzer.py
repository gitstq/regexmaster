"""
Regex pattern analyzer with explanation and visualization capabilities.
"""

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class Token:
    """Represents a parsed regex token."""

    type: str
    value: str
    description: str
    position: tuple[int, int]


class RegexAnalyzer:
    """
    Analyzes regex patterns and generates explanations.

    Features:
    - Pattern tokenization
    - Plain English explanations
    - AST tree visualization
    - Complexity analysis
    """

    # Token patterns and their descriptions
    TOKEN_PATTERNS = {
        # Character classes
        r"\\d": ("DIGIT", "Matches any digit (0-9)"),
        r"\\D": ("NON_DIGIT", "Matches any non-digit character"),
        r"\\w": ("WORD_CHAR", "Matches any word character (a-z, A-Z, 0-9, _)"),
        r"\\W": ("NON_WORD", "Matches any non-word character"),
        r"\\s": ("WHITESPACE", "Matches any whitespace character"),
        r"\\S": ("NON_WHITESPACE", "Matches any non-whitespace character"),
        r"\\.": ("DOT_ESCAPED", "Matches a literal dot"),
        r"\\n": ("NEWLINE", "Matches a newline character"),
        r"\\t": ("TAB", "Matches a tab character"),
        r"\\r": ("CARRIAGE_RETURN", "Matches a carriage return"),
        # Anchors
        r"^": ("START", "Matches the start of the string"),
        r"$": ("END", "Matches the end of the string"),
        r"\\b": ("WORD_BOUNDARY", "Matches a word boundary"),
        r"\\B": ("NON_BOUNDARY", "Matches a non-word boundary"),
        # Quantifiers
        r"\+\?": ("LAZY_ONE_OR_MORE", "Matches 1 or more (lazy)"),
        r"\*\?": ("LAZY_ZERO_OR_MORE", "Matches 0 or more (lazy)"),
        r"\?\?": ("LAZY_OPTIONAL", "Matches 0 or 1 (lazy)"),
        r"\{(\d+),(\d+)\}\?": ("LAZY_RANGE", "Matches between N and M times (lazy)"),
        r"\{(\d+)\}\?": ("LAZY_EXACT", "Matches exactly N times (lazy)"),
        r"\{(\d+),\}\?": ("LAZY_MIN", "Matches N or more times (lazy)"),
        r"\+": ("ONE_OR_MORE", "Matches 1 or more times"),
        r"\*": ("ZERO_OR_MORE", "Matches 0 or more times"),
        r"\?": ("OPTIONAL", "Matches 0 or 1 time"),
        r"\{(\d+),(\d+)\}": ("RANGE", "Matches between N and M times"),
        r"\{(\d+)\}": ("EXACT", "Matches exactly N times"),
        r"\{(\d+),\}": ("MIN", "Matches N or more times"),
        # Groups
        r"\(\?P<(\w+)>": ("NAMED_GROUP", "Named capturing group"),
        r"\(\?:": ("NON_CAPTURING", "Non-capturing group"),
        r"\(\?=": ("LOOKAHEAD", "Positive lookahead"),
        r"\(\?!": ("NEG_LOOKAHEAD", "Negative lookahead"),
        r"\(\?<=": ("LOOKBEHIND", "Positive lookbehind"),
        r"\(\?<!": ("NEG_LOOKBEHIND", "Negative lookbehind"),
        r"\(": ("GROUP", "Capturing group"),
        r"\)": ("GROUP_END", "End of group"),
        # Alternation
        r"\|": ("OR", "Alternation (OR)"),
        # Character class
        r"\[([^\]]+)\]": ("CHAR_CLASS", "Character class"),
        r"\[\^([^\]]+)\]": ("NEG_CHAR_CLASS", "Negated character class"),
        # Dot
        r"\.": ("DOT", "Matches any character except newline"),
        # Escape sequences
        r"\\([^\w])": ("ESCAPED", "Escaped special character"),
    }

    def __init__(self, pattern: str) -> None:
        """Initialize the analyzer with a pattern."""
        self.pattern = pattern
        self.tokens: list[Token] = []
        self._tokenize()

    def _tokenize(self) -> None:
        """Tokenize the regex pattern."""
        pos = 0
        pattern = self.pattern

        while pos < len(pattern):
            matched = False

            # Try to match each token pattern
            for regex, (token_type, description) in self.TOKEN_PATTERNS.items():
                try:
                    match = re.match(regex, pattern[pos:])
                    if match:
                        value = match.group(0)
                        self.tokens.append(
                            Token(
                                type=token_type,
                                value=value,
                                description=description,
                                position=(pos, pos + len(value)),
                            )
                        )
                        pos += len(value)
                        matched = True
                        break
                except re.error:
                    continue

            if not matched:
                # Literal character
                char = pattern[pos]
                self.tokens.append(
                    Token(
                        type="LITERAL",
                        value=char,
                        description=f"Matches the literal character '{char}'",
                        position=(pos, pos + 1),
                    )
                )
                pos += 1

    def explain(self) -> str:
        """
        Generate a plain English explanation of the pattern.

        Returns:
            Human-readable explanation
        """
        if not self.tokens:
            return "Empty pattern"

        lines = ["Pattern Breakdown:", "─" * 40]

        for i, token in enumerate(self.tokens, 1):
            lines.append(f"\n{i}. [cyan]{token.value}[/]")
            lines.append(f"   {token.description}")

        # Add overall summary
        lines.append("\n" + "─" * 40)
        lines.append("\nSummary:")
        summary = self._generate_summary()
        lines.append(summary)

        return "\n".join(lines)

    def _generate_summary(self) -> str:
        """Generate a summary of what the pattern matches."""
        has_start = any(t.type == "START" for t in self.tokens)
        has_end = any(t.type == "END" for t in self.tokens)
        has_digit = any(t.type == "DIGIT" for t in self.tokens)
        has_word = any(t.type == "WORD_CHAR" for t in self.tokens)
        has_whitespace = any(t.type == "WHITESPACE" for t in self.tokens)

        parts = []

        if has_start:
            parts.append("starts at the beginning")
        if has_digit:
            parts.append("contains digits")
        if has_word:
            parts.append("contains word characters")
        if has_whitespace:
            parts.append("may contain whitespace")
        if has_end:
            parts.append("ends at the end")

        if parts:
            return f"This pattern matches strings that {' and '.join(parts)}."
        return "This pattern matches specific text patterns."

    def get_ast_tree(self) -> str:
        """
        Generate an ASCII tree representation of the pattern structure.

        Returns:
            ASCII tree string
        """
        if not self.tokens:
            return "(empty)"

        lines = ["Pattern AST:", "└── Pattern"]

        for i, token in enumerate(self.tokens):
            prefix = "    ├── " if i < len(self.tokens) - 1 else "    └── "
            lines.append(f"{prefix}{token.type}: {token.value}")

        return "\n".join(lines)

    def get_complexity(self) -> str:
        """
        Analyze pattern complexity.

        Returns:
            Complexity level (Low, Medium, High)
        """
        score = 0

        # Count various elements
        groups = sum(1 for t in self.tokens if "GROUP" in t.type)
        quantifiers = sum(1 for t in self.tokens if t.type in ("ONE_OR_MORE", "ZERO_OR_MORE", "RANGE", "LAZY_ONE_OR_MORE", "LAZY_ZERO_OR_MORE"))
        lookarounds = sum(1 for t in self.tokens if "LOOKAHEAD" in t.type or "LOOKBEHIND" in t.type)
        alternations = sum(1 for t in self.tokens if t.type == "OR")

        score += groups * 2
        score += quantifiers * 3
        score += lookarounds * 4
        score += alternations * 2

        if score < 5:
            return "Low"
        elif score < 15:
            return "Medium"
        else:
            return "High"
