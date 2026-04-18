import argparse
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from .advisor import TechAdvisor

console = Console()

def display_solutions(result: dict):
    if "error" in result:
        console.print(f"[bold red]Error:[/bold red] {result['error']}")
        return

    console.print(Panel(f"[bold cyan]Requirement:[/bold cyan] {result['requirement']}", border_style="blue"))
    
    panels = []
    for sol in result['solutions']:
        is_rec = sol['id'] == result['recommendation']
        border = "green" if is_rec else "white"
        title = f"{'[REC] ' if is_rec else ''}{sol['name']}"
        
        content = f"{sol['description']}\n\n"
        content += f"[bold]Tech Stack:[/bold] {', '.join(sol['tech_stack'])}\n"
        content += f"[bold green]Pros:[/bold green] {', '.join(sol['pros'])}\n"
        content += f"[bold red]Cons:[/bold red] {', '.join(sol['cons'])}\n"
        content += f"[bold]Complexity:[/bold] {sol['complexity']} | [bold]Cost:[/bold] {sol['cost']} | [bold]Timeline:[/bold] {sol['timeline']}\n"
        content += f"[bold italic]Best for:[/bold italic] {sol['best_for']}"
        
        panels.append(Panel(content, title=title, border_style=border, expand=True))
    
    console.print(Columns(panels, equal=True))
    console.print(Panel(f"[bold green]Recommendation Reasoning:[/bold green]\n{result['recommendation_reasoning']}", border_style="green"))

def display_evaluation(result: dict):
    if "error" in result:
        console.print(f"[bold red]Error:[/bold red] {result['error']}")
        return

    score_color = "green" if result['overall_score'] >= 8 else "yellow" if result['overall_score'] >= 6 else "red"
    console.print(Panel(f"[bold]Solution:[/bold] {result['solution_name']}\n[bold]Overall Score:[/bold] [{score_color}]{result['overall_score']}/10[/{score_color}]\n[bold]Decision:[/bold] {result['decision']}", border_style="blue"))

    table = Table(title="Dimension Analysis", show_header=True, header_style="bold magenta")
    table.add_column("Dimension")
    table.add_column("Score")
    table.add_column("Analysis")
    
    for dim in result['dimensions']:
        d_color = "green" if dim['score'] >= 8 else "yellow" if dim['score'] >= 6 else "red"
        table.add_row(dim['name'], f"[{d_color}]{dim['score']}[/{d_color}]", dim['analysis'])
    
    console.print(table)
    
    for dim in result['dimensions']:
        if dim['risks'] or dim['suggestions']:
            console.print(f"\n[bold]{dim['name']} Details:[/bold]")
            if dim['risks']: console.print(f"  [red]Risks:[/red] {', '.join(dim['risks'])}")
            if dim['suggestions']: console.print(f"  [green]Suggestions:[/green] {', '.join(dim['suggestions'])}")

    console.print(Panel(f"[bold]Decision Reasoning:[/bold]\n{result['decision_reasoning']}", border_style="cyan"))
    if result.get('alternatives'):
        console.print(f"\n[bold]Alternatives:[/bold] {', '.join(result['alternatives'])}")

def main():
    parser = argparse.ArgumentParser(description="AI Tech Decision Advisor CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate technical solutions")
    gen_parser.add_argument("requirement", help="Requirement description")

    # Evaluate command
    eval_parser = subparsers.add_parser("evaluate", help="Evaluate technical solution")
    eval_parser.add_argument("solution", help="Solution description")

    args = parser.parse_args()

    try:
        advisor = TechAdvisor()
    except Exception as e:
        console.print(f"[bold red]Configuration Error:[/bold red] {str(e)}")
        sys.exit(1)

    if args.command == "generate":
        result = advisor.generate_solutions(args.requirement)
        display_solutions(result)
    elif args.command == "evaluate":
        result = advisor.evaluate_solution(args.solution)
        display_evaluation(result)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
