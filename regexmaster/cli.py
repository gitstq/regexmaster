#!/usr/bin/env python3
"""
RegexMaster CLI Entry Point.

A powerful terminal-based regex testing and debugging tool.
"""

import sys
from typing import Optional

import click
from rich.console import Console

console = Console()


@click.group(invoke_without_command=True)
@click.option("--version", "-v", is_flag=True, help="Show version and exit")
@click.option("--pattern", "-p", help="Regex pattern to test")
@click.option("--text", "-t", help="Test text")
@click.option("--ai", is_flag=True, help="Enable AI explanations")
@click.pass_context
def main(ctx: click.Context, version: bool, pattern: Optional[str], text: Optional[str], ai: bool) -> None:
    """
    🔍 RegexMaster - Terminal Regex Testing & Debugging Tool

    A powerful Python-based regex tool with AI-powered explanations,
    visual analysis, and performance optimization.

    \b
    Examples:
        regexmaster                    # Launch interactive TUI
        regexmaster -p '\\d+' -t '123'  # Quick test
        regexmaster --ai               # Launch with AI mode
    """
    if version:
        from regexmaster import __version__
        console.print(f"[bold green]RegexMaster[/] version {__version__}")
        return

    if ctx.invoked_subcommand is None:
        # Launch TUI
        from regexmaster.tui.app import RegexMasterApp

        app = RegexMasterApp(
            initial_pattern=pattern or "",
            initial_text=text or "",
            ai_enabled=ai,
        )
        app.run()


@main.command()
@click.argument("pattern")
@click.option("--text", "-t", required=True, help="Text to match")
@click.option("--explain", "-e", is_flag=True, help="Explain the pattern")
def test(pattern: str, text: str, explain: bool) -> None:
    """
    Quick test a regex pattern against text.

    \b
    Example:
        regexmaster test '\\d+' -t 'abc123def'
    """
    import re
    from regexmaster.core.engine import RegexEngine

    engine = RegexEngine(pattern)
    result = engine.match(text)

    console.print(f"\n[bold]Pattern:[/] [cyan]{pattern}[/]")
    console.print(f"[bold]Text:[/] {text}\n")

    if result.matches:
        console.print(f"[bold green]✓ Found {len(result.matches)} match(es)[/]\n")
        for i, match in enumerate(result.matches, 1):
            console.print(f"  {i}. [yellow]{match.group()}[/] (pos {match.start()}-{match.end()})")
            if match.groups():
                console.print(f"     Groups: {match.groups()}")
    else:
        console.print("[bold red]✗ No matches found[/]")

    if explain:
        from regexmaster.core.analyzer import RegexAnalyzer
        analyzer = RegexAnalyzer(pattern)
        explanation = analyzer.explain()
        console.print(f"\n[bold]Explanation:[/]\n{explanation}")


@main.command()
@click.argument("pattern")
def explain(pattern: str) -> None:
    """
    Explain a regex pattern in plain English.

    \b
    Example:
        regexmaster explain '\\d{3}-\\d{3}-\\d{4}'
    """
    from regexmaster.core.analyzer import RegexAnalyzer

    analyzer = RegexAnalyzer(pattern)
    explanation = analyzer.explain()

    console.print(f"\n[bold]Pattern:[/] [cyan]{pattern}[/]\n")
    console.print(f"[bold]Explanation:[/]\n{explanation}")


@main.command()
@click.argument("pattern")
@click.option("--language", "-l", default="python", help="Target language (python, javascript, go, java)")
def generate(pattern: str, language: str) -> None:
    """
    Generate code for a regex pattern.

    \b
    Example:
        regexmaster generate '\\d+' -l python
    """
    from regexmaster.core.engine import RegexEngine

    engine = RegexEngine(pattern)
    code = engine.generate_code(language)

    console.print(f"\n[bold]Generated {language.upper()} code:[/]\n")
    console.print(code)


@main.command()
@click.argument("pattern")
@click.option("--text", "-t", required=True, help="Text to analyze")
def optimize(pattern: str, text: str) -> None:
    """
    Analyze and suggest optimizations for a regex pattern.

    \b
    Example:
        regexmaster optimize '.*.*.*' -t 'test'
    """
    from regexmaster.core.optimizer import RegexOptimizer

    optimizer = RegexOptimizer(pattern)
    analysis = optimizer.analyze(text)

    console.print(f"\n[bold]Pattern:[/] [cyan]{pattern}[/]\n")
    console.print(f"[bold]Performance Analysis:[/]")
    console.print(f"  Match time: {analysis.match_time_ms:.3f}ms")
    console.print(f"  Complexity: {analysis.complexity}")

    if analysis.warnings:
        console.print(f"\n[bold yellow]⚠ Warnings:[/]")
        for warning in analysis.warnings:
            console.print(f"  • {warning}")

    if analysis.suggestions:
        console.print(f"\n[bold green]💡 Optimization Suggestions:[/]")
        for suggestion in analysis.suggestions:
            console.print(f"  • {suggestion}")


@main.command()
def learn() -> None:
    """
    Launch interactive regex tutorial.

    \b
    Example:
        regexmaster learn
    """
    from regexmaster.tui.app import LearningApp

    app = LearningApp()
    app.run()


if __name__ == "__main__":
    main()
