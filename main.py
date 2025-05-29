import typer
from rich.console import Console
from rich.progress import Progress
from pathlib import Path
from dotenv import load_dotenv
import os

from src.auth.instagram_client import InstagramClient
from src.data.user_loader import UserLoader
from src.services.dm_sender import DMSender
from src.utils.logger import setup_logger
from src.utils.csv_processor import process_category_files

# Initialize Typer app
app = typer.Typer(help="Instagram DM Automation Tool")
console = Console()

# Load environment variables
load_dotenv()

# Setup logger
logger = setup_logger()

@app.command()
def process_categories(
    output_file: str = typer.Option("data/users.csv", help="Path to output CSV file")
):
    """
    Process category CSV files and combine them into a single users file
    """
    try:
        if process_category_files(output_file):
            console.print(f"[green]Successfully processed category files to {output_file}[/green]")
        else:
            console.print("[red]Failed to process category files[/red]")
            raise typer.Exit(1)

    except Exception as e:
        logger.error(f"Error in process_categories: {str(e)}")
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)

@app.command()
def send_messages(
    users_file: str = typer.Option("data/users.csv", help="Path to users CSV file"),
    templates_file: str = typer.Option("data/message_templates.json", help="Path to message templates JSON file"),
    dry_run: bool = typer.Option(False, help="Run without sending actual messages")
):
    """
    Start sending DMs to users from the specified CSV file
    """
    try:
        # Initialize components
        client = InstagramClient()
        user_loader = UserLoader(users_file)
        dm_sender = DMSender(client, templates_file)

        # Load users
        users = user_loader.load_users()
        
        if not users:
            console.print("[red]No users found in the CSV file[/red]")
            raise typer.Exit(1)

        # Login to Instagram
        if not client.login():
            console.print("[red]Failed to login to Instagram[/red]")
            raise typer.Exit(1)

        console.print(f"[green]Found {len(users)} users to process[/green]")
        
        if dry_run:
            console.print("[yellow]Running in dry-run mode - no messages will be sent[/yellow]")

        # Process users
        with Progress() as progress:
            task = progress.add_task("[cyan]Sending messages...", total=len(users))
            
            for user in users:
                try:
                    if not dry_run:
                        success = dm_sender.send_message(user)
                        status = "[green]Success[/green]" if success else "[red]Failed[/red]"
                    else:
                        # Get template for category
                        template1 = dm_sender._get_template(user["category"], "template_1")
                        template2 = dm_sender._get_template(user["category"], "template_2")
                        
                        if template1 and template2:
                            console.print(f"\n[bold]Processing {user['username']} ({user['category']}):[/bold]")
                            console.print("[cyan]Message 1:[/cyan]")
                            console.print(template1["text"])
                            console.print("\n[cyan]Message 2:[/cyan]")
                            console.print(template2["text"])
                            console.print("---")
                        status = "[yellow]Dry run[/yellow]"
                    
                    console.print(f"Processing {user['username']}: {status}")
                except Exception as e:
                    logger.error(f"Error processing user {user['username']}: {str(e)}")
                    console.print(f"[red]Error processing {user['username']}: {str(e)}[/red]")
                
                progress.advance(task)

    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)

@app.command()
def show_stats():
    """
    Display sending statistics from the logs
    """
    try:
        log_file = Path("logs/sent_log.csv")
        if not log_file.exists():
            console.print("[yellow]No statistics available yet[/yellow]")
            return

        # TODO: Implement statistics display
        console.print("[green]Statistics feature coming soon![/green]")

    except Exception as e:
        console.print(f"[red]Error showing statistics: {str(e)}[/red]")
        raise typer.Exit(1)

@app.command()
def test_connection():
    """
    Test Instagram connection and authentication
    """
    try:
        client = InstagramClient()
        if client.login():
            console.print("[green]Successfully connected to Instagram![/green]")
        else:
            console.print("[red]Failed to connect to Instagram[/red]")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[red]Connection test failed: {str(e)}[/red]")
        raise typer.Exit(1)

@app.command()
def clear_logs():
    """
    Clear log files
    """
    try:
        log_files = ["logs/app.log", "logs/sent_log.csv"]
        for file in log_files:
            if os.path.exists(file):
                os.remove(file)
                console.print(f"[green]Cleared {file}[/green]")
            else:
                console.print(f"[yellow]{file} does not exist[/yellow]")

    except Exception as e:
        console.print(f"[red]Error clearing logs: {str(e)}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app() 