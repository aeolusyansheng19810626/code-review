import argparse
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from reviewer import CodeReviewer

console = Console()

def display_review(result: dict):
    if "error" in result:
        console.print(f"[bold red]Error:[/bold red] {result['error']}")
        return

    # Summary Panel
    score_color = "green" if result['score'] >= 8 else "yellow" if result['score'] >= 6 else "red"
    summary_text = f"[bold]Score:[/bold] [{score_color}]{result['score']}/10[/{score_color}]\n[bold]Summary:[/bold] {result['summary']}"
    console.print(Panel(summary_text, title="Review Summary", border_style="blue"))

    # Strengths
    if result.get('strengths'):
        console.print("\n[bold green]Strengths:[/bold green]")
        for strength in result['strengths']:
            console.print(f"  • {strength}")

    # Issues Table
    if result.get('issues'):
        table = Table(title="Issues Identified", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim")
        table.add_column("Category")
        table.add_column("Severity")
        table.add_column("Line")
        table.add_column("Description")

        for issue in result['issues']:
            sev_color = "red" if issue['severity'] == "严重" else "yellow" if issue['severity'] == "中" else "blue"
            table.add_row(
                str(issue['id']),
                issue['category'],
                f"[{sev_color}]{issue['severity']}[/{sev_color}]",
                str(issue['line']) if issue['line'] else "N/A",
                issue['description']
            )
            # Add suggestion and code fix as sub-info?
        console.print(table)
        
        for issue in result['issues']:
            if issue.get('code_fix'):
                console.print(Panel(
                    Syntax(issue['code_fix'], "python", theme="monokai", line_numbers=True),
                    title=f"Fix for Issue #{issue['id']}",
                    border_style="green"
                ))

    # Overall Suggestion
    if result.get('overall_suggestion'):
        console.print(Panel(result['overall_suggestion'], title="Overall Suggestion", border_style="cyan"))

def main():
    parser = argparse.ArgumentParser(description="AI Code Reviewer CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Review command
    review_parser = subparsers.add_parser("review", help="Review code")
    review_parser.add_argument("file", nargs="?", help="File to review")
    review_parser.add_argument("--code", help="Inline code to review")

    args = parser.parse_args()

    try:
        reviewer = CodeReviewer()
    except Exception as e:
        console.print(f"[bold red]Configuration Error:[/bold red] {str(e)}")
        sys.exit(1)

    if args.command == "review":
        if args.code:
            result = reviewer.review_code(args.code)
        elif args.file:
            result = reviewer.review_file(args.file)
        else:
            review_parser.print_help()
            sys.exit(1)
        
        display_review(result)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
