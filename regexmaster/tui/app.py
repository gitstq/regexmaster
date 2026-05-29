"""
RegexMaster TUI Application.

A beautiful terminal user interface for regex testing and debugging.
"""

from typing import Optional

from rich.text import Text
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Label,
    Static,
    TabbedContent,
    TabPane,
    TextArea,
)


class PatternInput(Input):
    """Pattern input widget."""

    def __init__(self, initial_pattern: str = "", **kwargs) -> None:
        super().__init__(
            placeholder="Enter regex pattern...",
            value=initial_pattern,
            **kwargs,
        )


class TestTextInput(TextArea):
    """Test text input widget."""

    def __init__(self, initial_text: str = "", **kwargs) -> None:
        super().__init__(
            initial_text,
            language="text",
            **kwargs,
        )


class MatchResults(Static):
    """Widget to display match results."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._results_text = ""

    def update_results(self, matches: list, pattern: str, text: str) -> None:
        """Update the displayed results."""
        if not matches:
            self.update(Text("No matches found", style="bold red"))
            return

        result_text = Text()
        result_text.append(f"Found {len(matches)} match(es)\n\n", style="bold green")

        for i, match in enumerate(matches, 1):
            result_text.append(f"Match {i}: ", style="bold cyan")
            result_text.append(f"'{match.group()}'\n")
            result_text.append(f"  Position: {match.start()}-{match.end()}\n")

            if match.groups():
                result_text.append(f"  Groups: {match.groups()}\n")

            result_text.append("\n")

        self.update(result_text)


class ExplanationPanel(Static):
    """Widget to display pattern explanation."""

    def update_explanation(self, explanation: str) -> None:
        """Update the explanation display."""
        self.update(Text(explanation))


class RegexMasterApp(App):
    """
    RegexMaster TUI Application.

    A powerful terminal-based regex testing and debugging tool.

    Features:
    - Real-time matching
    - Pattern explanation
    - Performance analysis
    - Code generation
    """

    CSS = """
    Screen {
        background: $surface;
    }

    .header {
        text-align: center;
        text-style: bold;
        color: $primary;
        padding: 1;
    }

    .pattern-container {
        height: 3;
        margin: 1;
    }

    .test-text-container {
        height: 40%;
        margin: 1;
    }

    .results-container {
        height: 40%;
        margin: 1;
    }

    PatternInput {
        width: 100%;
        height: 3;
    }

    TestTextInput {
        width: 100%;
        height: 100%;
    }

    MatchResults {
        width: 100%;
        height: 100%;
        overflow: auto;
    }

    TabbedContent {
        height: 100%;
    }

    Button {
        margin: 1;
    }

    .status-bar {
        dock: bottom;
        height: 1;
        background: $panel;
        color: $text;
    }
    """

    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+e", "explain", "Explain"),
        ("ctrl+g", "generate_code", "Generate Code"),
        ("ctrl+o", "optimize", "Optimize"),
        ("ctrl+l", "clear", "Clear"),
        ("f1", "help", "Help"),
    ]

    def __init__(
        self,
        initial_pattern: str = "",
        initial_text: str = "",
        ai_enabled: bool = False,
    ) -> None:
        super().__init__()
        self.initial_pattern = initial_pattern
        self.initial_text = initial_text
        self.ai_enabled = ai_enabled

    def compose(self) -> ComposeResult:
        """Compose the UI."""
        yield Header()

        with Container():
            with Container(classes="pattern-container"):
                yield Label("🔍 Pattern:", classes="header")
                yield PatternInput(self.initial_pattern, id="pattern-input")

            with TabbedContent(initial="test"):
                with TabPane("Test", id="test"):
                    with Vertical():
                        with Container(classes="test-text-container"):
                            yield Label("📝 Test Text:", classes="header")
                            yield TestTextInput(self.initial_text, id="test-text")

                        with Container(classes="results-container"):
                            yield Label("✨ Results:", classes="header")
                            yield MatchResults(id="match-results")

                with TabPane("Explain", id="explain"):
                    yield ExplanationPanel(id="explanation-panel")

                with TabPane("Optimize", id="optimize"):
                    yield Static("Performance analysis will appear here", id="optimize-panel")

                with TabPane("Code", id="code"):
                    yield Static("Generated code will appear here", id="code-panel")

        yield Footer()

    def on_mount(self) -> None:
        """Handle app mount."""
        self.title = "RegexMaster"
        self.sub_title = "Terminal Regex Testing & Debugging"

        # Focus pattern input
        pattern_input = self.query_one("#pattern-input", PatternInput)
        pattern_input.focus()

        # Start watching for changes
        pattern_input.on_change = self._on_pattern_change

    def _on_pattern_change(self, value: str) -> None:
        """Handle pattern input changes."""
        self._update_matches()

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes."""
        if event.input.id == "pattern-input":
            self._update_matches()

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        """Handle text area changes."""
        if event.text_area.id == "test-text":
            self._update_matches()

    def _update_matches(self) -> None:
        """Update match results."""
        pattern_input = self.query_one("#pattern-input", PatternInput)
        test_text = self.query_one("#test-text", TestTextInput)
        results = self.query_one("#match-results", MatchResults)

        pattern = pattern_input.value
        text = test_text.text

        if not pattern or not text:
            results.update_results([], pattern, text)
            return

        from regexmaster.core.engine import RegexEngine

        engine = RegexEngine(pattern)

        if not engine.is_valid:
            results.update(Text(f"Invalid pattern: {engine.error}", style="bold red"))
            return

        result = engine.match(text)
        results.update_results(result.matches, pattern, text)

    def action_explain(self) -> None:
        """Explain the current pattern."""
        pattern_input = self.query_one("#pattern-input", PatternInput)
        explanation_panel = self.query_one("#explanation-panel", ExplanationPanel)

        pattern = pattern_input.value

        if not pattern:
            explanation_panel.update_explanation("Enter a pattern to see explanation")
            return

        from regexmaster.core.analyzer import RegexAnalyzer

        analyzer = RegexAnalyzer(pattern)
        explanation = analyzer.explain()

        explanation_panel.update_explanation(explanation)

        # Switch to explain tab
        tabbed = self.query_one(TabbedContent)
        tabbed.active = "explain"

    def action_generate_code(self) -> None:
        """Generate code for the current pattern."""
        pattern_input = self.query_one("#pattern-input", PatternInput)
        code_panel = self.query_one("#code-panel", Static)

        pattern = pattern_input.value

        if not pattern:
            code_panel.update("Enter a pattern to generate code")
            return

        from regexmaster.core.engine import RegexEngine

        engine = RegexEngine(pattern)
        code = engine.generate_code("python")

        code_panel.update(Text(code, style="cyan"))

        # Switch to code tab
        tabbed = self.query_one(TabbedContent)
        tabbed.active = "code"

    def action_optimize(self) -> None:
        """Analyze and optimize the current pattern."""
        pattern_input = self.query_one("#pattern-input", PatternInput)
        test_text = self.query_one("#test-text", TestTextInput)
        optimize_panel = self.query_one("#optimize-panel", Static)

        pattern = pattern_input.value

        if not pattern:
            optimize_panel.update("Enter a pattern to analyze")
            return

        from regexmaster.core.optimizer import RegexOptimizer

        optimizer = RegexOptimizer(pattern)
        result = optimizer.analyze(test_text.text)

        analysis = Text()
        analysis.append("Performance Analysis\n", style="bold")
        analysis.append("─" * 40 + "\n\n")
        analysis.append(f"Complexity: {result.complexity}\n", style="cyan")
        analysis.append(f"Match Time: {result.match_time_ms:.3f}ms\n\n", style="cyan")

        if result.warnings:
            analysis.append("⚠ Warnings:\n", style="bold yellow")
            for warning in result.warnings:
                analysis.append(f"  • {warning}\n")
            analysis.append("\n")

        if result.suggestions:
            analysis.append("💡 Suggestions:\n", style="bold green")
            for suggestion in result.suggestions:
                analysis.append(f"  • {suggestion}\n")

        optimize_panel.update(analysis)

        # Switch to optimize tab
        tabbed = self.query_one(TabbedContent)
        tabbed.active = "optimize"

    def action_clear(self) -> None:
        """Clear all inputs."""
        pattern_input = self.query_one("#pattern-input", PatternInput)
        test_text = self.query_one("#test-text", TestTextInput)

        pattern_input.value = ""
        test_text.text = ""

    def action_help(self) -> None:
        """Show help."""
        self.push_screen("help")


class LearningApp(App):
    """Interactive regex learning application."""

    CSS = """
    Screen {
        background: $surface;
    }

    .lesson {
        padding: 2;
    }
    """

    def compose(self) -> ComposeResult:
        """Compose the learning UI."""
        yield Header()
        yield Container(
            Label("📚 Regex Learning Mode", classes="header"),
            Static("Interactive lessons coming soon..."),
            classes="lesson",
        )
        yield Footer()

    def on_mount(self) -> None:
        """Handle mount."""
        self.title = "RegexMaster - Learning Mode"
