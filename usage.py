import os
import sys
import json
import subprocess

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.theme import Theme
    from rich.progress import Progress, BarColumn, TextColumn
    from rich.table import Table
except ImportError:
    print("Installing rich...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rich", "--quiet"])
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.theme import Theme
    from rich.progress import Progress, BarColumn, TextColumn
    from rich.table import Table

# Set UTF-8 encoding for Windows console to prevent charmap crashes
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

custom_theme = Theme({
    "info": "bold white",
    "danger": "bold red",
    "success": "bold green",
})
console = Console(theme=custom_theme)

BUDGET_LIMIT = 30.00

def fetch_billing_data():
    try:
        # Run the modal billing report command
        result = subprocess.run(
            ["modal", "billing", "report", "--for", "this month", "--json"],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
        return data
    except Exception as e:
        console.print(f"[danger]✖ Failed to fetch billing data from Modal: {e}[/danger]")
        sys.exit(1)

def main():
    console.print("\n[italic dim white]Fetching live billing data from Modal...[/italic dim white]")
    data = fetch_billing_data()
    
    total_cost = 0.0
    openmodal_cost = 0.0
    
    for item in data:
        cost = float(item.get("cost", 0.0))
        total_cost += cost
        
        # Track OpenModal specific costs (the class server and the endpoint)
        desc = item.get("description", "").lower()
        if "gemma" in desc or "openmodal" in desc:
            openmodal_cost += cost

    # Build the UI
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Title
    title = Text("OPENMODAL USAGE & COST MONITOR", style="bold red")
    
    # Table of costs
    table = Table(show_header=False, box=None, padding=(0, 4))
    table.add_column("Category", style="bold white")
    table.add_column("Cost", style="bold red", justify="right")
    
    table.add_row("Total Workspace Cost:", f"${total_cost:.4f}")
    table.add_row("OpenModal API Cost:", f"${openmodal_cost:.4f}")
    
    # Progress Bar against $30 limit
    pct_used = (total_cost / BUDGET_LIMIT) * 100
    if pct_used > 100: pct_used = 100
    
    progress = Progress(
        TextColumn("[bold white]Budget Usage:[/bold white]"),
        BarColumn(bar_width=40, style="white", complete_style="red"),
        TextColumn("[bold red]{task.percentage:>3.1f}%[/bold red]"),
        TextColumn(f"[bold white](${total_cost:.2f} / ${BUDGET_LIMIT:.2f})[/bold white]")
    )
    task = progress.add_task("budget", total=BUDGET_LIMIT, completed=total_cost)

    # Put it all together
    from rich.console import Group
    group = Group(
        table,
        Text(""),
        progress
    )
    
    console.print(Panel(group, title=title, border_style="red", padding=(1, 2)))

if __name__ == "__main__":
    main()
