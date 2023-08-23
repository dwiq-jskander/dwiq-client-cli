from google.cloud import bigquery
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

# TODO: Remove hardcoded values in favor of envs
PROJECT_ID = "test-database-31b0"
DATASET_ID = "test_database_31b0_dataset"
TABLE_ID = "all_client_list"

app = typer.Typer()

@app.command()
def domain(
    search_term: str,
    exact: bool = typer.Option(False, "--exact", help="Search for exact match")
    ) -> None:
    """Search for string match against client domains"""

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Processing...", total=None)

        client = bigquery.Client()

        if exact:
            condition = f"url = '{search_term}'"
        else:
            condition = f"url LIKE '%{search_term}%'"

        query = f"""
            SELECT *
            FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
            WHERE {condition}
        """

        query_job = client.query(query)
        results = query_job.result()

        table = Table(title="Domain search results")
        table.add_column("Company")
        table.add_column("URL")
        table.add_column("Source")
        table.add_column("Notification")
        table.add_column("Intervention")
        table.add_column("Group Ref")
        table.add_column("Policy Ref")
        for r in results:
            table.add_row(*r.values())

        console = Console()
        console.print(table)

if __name__ == "__main__":
    app()
