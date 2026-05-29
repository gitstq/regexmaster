"""
Core regex engine with matching, analysis, and code generation capabilities.
"""

import re
import time
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class MatchResult:
    """Result of a regex match operation."""

    matches: list[re.Match[str]] = field(default_factory=list)
    groups: dict[int, str] = field(default_factory=dict)
    named_groups: dict[str, str] = field(default_factory=dict)
    match_time_ms: float = 0.0
    error: Optional[str] = None


@dataclass
class CodeTemplate:
    """Generated code template."""

    language: str
    code: str
    imports: list[str] = field(default_factory=list)


class RegexEngine:
    """
    Advanced regex engine with matching, analysis, and code generation.

    Features:
    - Pattern compilation with error handling
    - Match result extraction
    - Code generation for multiple languages
    - Performance timing
    """

    def __init__(self, pattern: str, flags: int = 0) -> None:
        """Initialize the regex engine with a pattern."""
        self.pattern = pattern
        self.flags = flags
        self._compiled: Optional[re.Pattern[str]] = None
        self._error: Optional[str] = None

        try:
            self._compiled = re.compile(pattern, flags)
        except re.error as e:
            self._error = str(e)

    @property
    def is_valid(self) -> bool:
        """Check if the pattern is valid."""
        return self._compiled is not None

    @property
    def error(self) -> Optional[str]:
        """Get the compilation error, if any."""
        return self._error

    def match(self, text: str) -> MatchResult:
        """
        Match the pattern against text.

        Args:
            text: The text to match against

        Returns:
            MatchResult with matches and timing information
        """
        result = MatchResult()

        if not self._compiled:
            result.error = self._error
            return result

        start_time = time.perf_counter()

        try:
            matches = list(self._compiled.finditer(text))
            result.matches = matches

            if matches:
                first_match = matches[0]
                result.groups = dict(enumerate(first_match.groups(), 1))
                result.named_groups = first_match.groupdict()

        except Exception as e:
            result.error = str(e)

        result.match_time_ms = (time.perf_counter() - start_time) * 1000
        return result

    def find_all(self, text: str) -> list[str]:
        """Find all matches in text."""
        if not self._compiled:
            return []
        return self._compiled.findall(text)

    def replace(self, text: str, replacement: str) -> str:
        """Replace all matches in text."""
        if not self._compiled:
            return text
        return self._compiled.sub(replacement, text)

    def split(self, text: str, maxsplit: int = 0) -> list[str]:
        """Split text by the pattern."""
        if not self._compiled:
            return [text]
        return self._compiled.split(text, maxsplit)

    def generate_code(self, language: str = "python") -> str:
        """
        Generate code for this regex pattern.

        Args:
            language: Target language (python, javascript, go, java)

        Returns:
            Generated code string
        """
        generators = {
            "python": self._generate_python,
            "javascript": self._generate_javascript,
            "js": self._generate_javascript,
            "go": self._generate_go,
            "golang": self._generate_go,
            "java": self._generate_java,
            "csharp": self._generate_csharp,
            "c#": self._generate_csharp,
        }

        generator = generators.get(language.lower(), self._generate_python)
        return generator()

    def _generate_python(self) -> str:
        """Generate Python code."""
        escaped_pattern = self.pattern.replace("\\", "\\\\")
        return f'''import re

# Pattern: {escaped_pattern}
pattern = re.compile(r"{escaped_pattern}")

# Example usage
text = "Your text here"
matches = pattern.findall(text)

for match in matches:
    print(match)
'''

    def _generate_javascript(self) -> str:
        """Generate JavaScript code."""
        return f'''// Pattern: {self.pattern}
const pattern = /{self.pattern}/g;

// Example usage
const text = "Your text here";
const matches = text.match(pattern);

if (matches) {{
    matches.forEach(match => console.log(match));
}}
'''

    def _generate_go(self) -> str:
        """Generate Go code."""
        escaped = self.pattern.replace('"', '\\"')
        return f'''package main

import (
    "fmt"
    "regexp"
)

func main() {{
    // Pattern: {escaped}
    pattern := regexp.MustCompile(`{escaped}`)

    text := "Your text here"
    matches := pattern.FindAllString(text, -1)

    for _, match := range matches {{
        fmt.Println(match)
    }}
}}
'''

    def _generate_java(self) -> str:
        """Generate Java code."""
        escaped = self.pattern.replace("\\", "\\\\").replace('"', '\\"')
        return f'''import java.util.regex.*;
import java.util.*;

public class RegexExample {{
    public static void main(String[] args) {{
        // Pattern: {escaped}
        Pattern pattern = Pattern.compile("{escaped}");

        String text = "Your text here";
        Matcher matcher = pattern.matcher(text);

        while (matcher.find()) {{
            System.out.println(matcher.group());
        }}
    }}
}}
'''

    def _generate_csharp(self) -> str:
        """Generate C# code."""
        escaped = self.pattern.replace("\\", "\\\\").replace('"', '\\"')
        return f'''using System;
using System.Text.RegularExpressions;

class Program {{
    static void Main() {{
        // Pattern: {escaped}
        var pattern = new Regex(@"{escaped}");

        string text = "Your text here";
        var matches = pattern.Matches(text);

        foreach (Match match in matches) {{
            Console.WriteLine(match.Value);
        }}
    }}
}}
'''
