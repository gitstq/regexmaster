"""
Tests for RegexMaster core engine.
"""

import pytest

from regexmaster.core.engine import MatchResult, RegexEngine


class TestRegexEngine:
    """Tests for RegexEngine class."""

    def test_valid_pattern(self) -> None:
        """Test valid pattern compilation."""
        engine = RegexEngine(r"\d+")
        assert engine.is_valid
        assert engine.error is None

    def test_invalid_pattern(self) -> None:
        """Test invalid pattern handling."""
        engine = RegexEngine(r"[unclosed")
        assert not engine.is_valid
        assert engine.error is not None

    def test_match_simple(self) -> None:
        """Test simple matching."""
        engine = RegexEngine(r"\d+")
        result = engine.match("abc123def")

        assert result.error is None
        assert len(result.matches) == 1
        assert result.matches[0].group() == "123"

    def test_match_multiple(self) -> None:
        """Test multiple matches."""
        engine = RegexEngine(r"\d+")
        result = engine.match("123 456 789")

        assert len(result.matches) == 3

    def test_match_no_match(self) -> None:
        """Test no match case."""
        engine = RegexEngine(r"\d+")
        result = engine.match("abc def")

        assert len(result.matches) == 0

    def test_match_groups(self) -> None:
        """Test capturing groups."""
        engine = RegexEngine(r"(\d+)-(\d+)")
        result = engine.match("123-456")

        assert result.groups[1] == "123"
        assert result.groups[2] == "456"

    def test_match_named_groups(self) -> None:
        """Test named capturing groups."""
        engine = RegexEngine(r"(?P<area>\d{3})-(?P<exchange>\d{3})-(?P<number>\d{4})")
        result = engine.match("555-123-4567")

        assert result.named_groups["area"] == "555"
        assert result.named_groups["exchange"] == "123"
        assert result.named_groups["number"] == "4567"

    def test_find_all(self) -> None:
        """Test findall method."""
        engine = RegexEngine(r"\d+")
        matches = engine.find_all("123 456 789")

        assert matches == ["123", "456", "789"]

    def test_replace(self) -> None:
        """Test replace method."""
        engine = RegexEngine(r"\d+")
        result = engine.replace("abc123def456", "X")

        assert result == "abcXdefX"

    def test_split(self) -> None:
        """Test split method."""
        engine = RegexEngine(r"\s+")
        result = engine.split("a b c")

        assert result == ["a", "b", "c"]

    def test_generate_python_code(self) -> None:
        """Test Python code generation."""
        engine = RegexEngine(r"\d+")
        code = engine.generate_code("python")

        assert "import re" in code
        assert r"\d+" in code

    def test_generate_javascript_code(self) -> None:
        """Test JavaScript code generation."""
        engine = RegexEngine(r"\d+")
        code = engine.generate_code("javascript")

        assert "const pattern" in code
        assert r"\d+" in code

    def test_generate_go_code(self) -> None:
        """Test Go code generation."""
        engine = RegexEngine(r"\d+")
        code = engine.generate_code("go")

        assert "package main" in code
        assert "regexp" in code

    def test_generate_java_code(self) -> None:
        """Test Java code generation."""
        engine = RegexEngine(r"\d+")
        code = engine.generate_code("java")

        assert "import java.util.regex" in code
        assert "Pattern.compile" in code

    def test_match_timing(self) -> None:
        """Test that match timing is recorded."""
        engine = RegexEngine(r"\d+")
        result = engine.match("123")

        assert result.match_time_ms >= 0


class TestMatchResult:
    """Tests for MatchResult dataclass."""

    def test_default_values(self) -> None:
        """Test default initialization."""
        result = MatchResult()

        assert result.matches == []
        assert result.groups == {}
        assert result.named_groups == {}
        assert result.match_time_ms == 0.0
        assert result.error is None
