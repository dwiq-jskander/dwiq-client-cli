import typer

from darkwebiq.cli import search

app = typer.Typer()
app.add_typer(search.app, name="search")

if __name__ == "__main__":
    app()