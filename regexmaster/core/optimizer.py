"""
Regex pattern optimizer with performance analysis and suggestions.
"""

import re
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class OptimizationResult:
    """Result of optimization analysis."""

    match_time_ms: float = 0.0
    complexity: str = "Low"
    warnings: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    optimized_pattern: Optional[str] = None
    improvement_percent: float = 0.0


class RegexOptimizer:
    """
    Analyzes regex patterns for performance issues and suggests optimizations.

    Features:
    - Performance timing
    - Catastrophic backtracking detection
    - Optimization suggestions
    - Pattern simplification
    """

    # Patterns that may cause catastrophic backtracking
    DANGEROUS_PATTERNS = [
        (r"\.\*\.\*", "Nested greedy quantifiers can cause exponential backtracking"),
        (r"\.\+\.\+", "Nested greedy quantifiers can cause exponential backtracking"),
        (r"\.\*\.\*\?", "Nested quantifiers (even lazy) can cause issues"),
        (r"\.\+\.\+\?", "Nested quantifiers (even lazy) can cause issues"),
        (r"\(\.\*\)\1", "Backreferences with .* can be slow"),
        (r"\(\.\+\)\1", "Backreferences with .+ can be slow"),
    ]

    # Common optimization opportunities
    OPTIMIZATIONS = [
        (r"\[0-9\]", r"\\d", "Use \\d instead of [0-9]"),
        (r"\[a-zA-Z0-9_\]", r"\\w", "Use \\w instead of [a-zA-Z0-9_]"),
        (r"\[a-zA-Z\]", r"[a-z] with re.IGNORECASE", "Use case-insensitive flag"),
        (r"\.\*\?$", r"\.?$", "Simplify .*? at end to .?"),
        (r"^\.\*", r"", "Remove leading .* if not needed"),
        (r"\.\*$", r"", "Remove trailing .* if not needed"),
        (r"\(\?:\)", r"", "Remove empty non-capturing groups"),
        (r"\(\)", r"", "Remove empty groups"),
    ]

    def __init__(self, pattern: str) -> None:
        """Initialize the optimizer with a pattern."""
        self.pattern = pattern
        self._compiled: Optional[re.Pattern[str]] = None

        try:
            self._compiled = re.compile(pattern)
        except re.error:
            pass

    def analyze(self, test_text: str = "", iterations: int = 1000) -> OptimizationResult:
        """
        Analyze the pattern for performance issues.

        Args:
            test_text: Text to use for timing tests
            iterations: Number of iterations for timing

        Returns:
            OptimizationResult with analysis
        """
        result = OptimizationResult()

        if not self._compiled:
            result.warnings.append("Invalid regex pattern")
            return result

        # Check for dangerous patterns
        for pattern, warning in self.DANGEROUS_PATTERNS:
            if re.search(pattern, self.pattern):
                result.warnings.append(warning)

        # Check for optimization opportunities
        for pattern, replacement, suggestion in self.OPTIMIZATIONS:
            if re.search(pattern, self.pattern):
                result.suggestions.append(suggestion)

        # Measure performance
        if test_text:
            result.match_time_ms = self._measure_performance(test_text, iterations)

        # Check for common issues
        self._check_common_issues(result)

        # Calculate complexity
        result.complexity = self._calculate_complexity()

        return result

    def _measure_performance(self, text: str, iterations: int) -> float:
        """Measure match performance."""
        if not self._compiled:
            return 0.0

        # Warm up
        for _ in range(10):
            self._compiled.search(text)

        # Measure
        start = time.perf_counter()
        for _ in range(iterations):
            self._compiled.search(text)
        end = time.perf_counter()

        return ((end - start) / iterations) * 1000

    def _check_common_issues(self, result: OptimizationResult) -> None:
        """Check for common regex issues."""
        pattern = self.pattern

        # Check for unescaped special characters
        if re.search(r"(?<!\\)\.(?![*+?{])", pattern):
            pass  # Dot is intentional

        # Check for redundant escapes
        if re.search(r"\\[a-zA-Z0-9](?![*+?{])", pattern):
            result.suggestions.append("Consider if escape sequences are necessary")

        # Check for overly broad patterns
        if re.search(r"^\.\*$", pattern):
            result.warnings.append("Pattern matches everything - consider being more specific")

        # Check for missing anchors
        if not pattern.startswith("^") and not pattern.endswith("$"):
            result.suggestions.append("Consider adding anchors (^ or $) for more precise matching")

        # Check for capturing groups that could be non-capturing
        group_count = pattern.count("(") - pattern.count("(?:")
        if group_count > 3:
            result.suggestions.append("Consider using non-capturing groups (?:...) if you don't need the captured values")

    def _calculate_complexity(self) -> str:
        """Calculate pattern complexity."""
        pattern = self.pattern

        score = 0

        # Count quantifiers
        score += pattern.count("*") * 2
        score += pattern.count("+") * 2
        score += pattern.count("?")
        score += pattern.count("{") * 2

        # Count groups
        score += pattern.count("(") * 3

        # Count alternations
        score += pattern.count("|") * 2

        # Count lookarounds
        score += pattern.count("(?=") * 4
        score += pattern.count("(?!") * 4
        score += pattern.count("(?<=") * 4
        score += pattern.count("(?<!") * 4

        # Count backreferences
        score += len(re.findall(r"\\[1-9]", pattern)) * 3

        if score < 10:
            return "Low"
        elif score < 25:
            return "Medium"
        else:
            return "High"

    def optimize(self) -> Optional[str]:
        """
        Attempt to optimize the pattern.

        Returns:
            Optimized pattern or None if no optimization possible
        """
        optimized = self.pattern

        for pattern, replacement, _ in self.OPTIMIZATIONS:
            optimized = re.sub(pattern, replacement, optimized)

        if optimized != self.pattern:
            return optimized

        return None

    def suggest_alternatives(self) -> list[str]:
        """
        Suggest alternative patterns that might be more efficient.

        Returns:
            List of alternative patterns
        """
        alternatives = []

        # Suggest using raw strings
        if "\\" in self.pattern and not self.pattern.startswith("r"):
            alternatives.append(f"Use raw string: r'{self.pattern}'")

        # Suggest re.IGNORECASE for case-insensitive matching
        if re.search(r"[a-zA-Z]", self.pattern) and not re.search(r"[A-Z].*[a-z]|[a-z].*[A-Z]", self.pattern):
            alternatives.append("Consider using re.IGNORECASE flag for case-insensitive matching")

        # Suggest re.DOTALL for matching newlines
        if re.search(r"\.\*", self.pattern) and "\n" not in self.pattern:
            alternatives.append("Consider using re.DOTALL flag if you need to match newlines with .")

        # Suggest re.MULTILINE for line-by-line matching
        if "^" in self.pattern or "$" in self.pattern:
            alternatives.append("Consider using re.MULTILINE flag for line-by-line matching")

        return alternatives
