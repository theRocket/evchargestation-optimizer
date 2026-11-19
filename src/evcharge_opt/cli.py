import typer
from rich.console import Console

app = typer.Typer(
    help="National EV Corridor Optimization CLI",
    no_args_is_help=True,
)
console = Console()


@app.callback()
def main() -> None:
    """National EV Corridor Optimization Pipeline."""


@app.command()
def info() -> None:
    """Display active pipeline configuration."""
    from evcharge_opt.config import settings

    console.print(
        f"[bold green]EV Charge Optimizer[/bold green] | "
        f"H3 Res: {settings.default_h3_resolution} | "
        f"Buffer: {settings.cross_border_buffer_km} km"
    )


if __name__ == "__main__":
    app()