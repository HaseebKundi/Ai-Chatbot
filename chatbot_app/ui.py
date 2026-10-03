"""Terminal interface built with `rich` (loading spinner, markdown, panels)."""
from __future__ import annotations

from rich.console import Console
from rich.markdown import Markdown
from rich.markup import escape
from rich.panel import Panel


class ChatUI:
    def __init__(self):
        self.console = Console()

    def banner(self, model: str) -> None:
        self.console.print(
            Panel.fit(
                "[bold cyan]Nova - AI Mentor[/]\n"
                f"[dim]Model: {escape(model)}[/]\n"
                "[dim]Type /help for commands[/]",
                border_style="cyan",
            )
        )

    def help(self) -> None:
        self.console.print(
            "[bold]Commands[/]\n"
            "  /clear  start a new conversation (forget history)\n"
            "  /help   show this help\n"
            "  /exit   quit\n"
        )

    def prompt(self) -> str:
        return self.console.input("[bold green]You:[/] ")

    def thinking(self):
        """Loading state: use as `with ui.thinking(): ...`"""
        return self.console.status("[cyan]Nova is thinking...[/]", spinner="dots")

    def show_reply(self, text: str) -> None:
        self.console.print(
            Panel(Markdown(text), title="Nova", title_align="left", border_style="cyan")
        )

    def show_error(self, message: str) -> None:
        self.console.print(f"[bold red]Error:[/] {escape(message)}\n")

    def warn(self, message: str) -> None:
        self.console.print(f"[yellow]{escape(message)}[/]\n")

    def info(self, message: str) -> None:
        self.console.print(f"[dim]{escape(message)}[/]\n")
