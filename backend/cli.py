import typer
import httpx
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint
from typing import Optional, List
import json
from enum import Enum
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import clear
from prompt_toolkit.formatted_text import HTML

app = typer.Typer(help="4X Space Empire Game Debug CLI")
console = Console()

# Default API URL
API_URL = "http://localhost:8000/api/v1"

class Format(str, Enum):
    json = "json"
    table = "table"

def get_api_url() -> str:
    """Get the API URL with environment variable support."""
    import os
    return os.getenv("API_URL", API_URL)

class InteractiveCLI:
    def __init__(self):
        self.commands = {
            'player': self.player,
            'planet': self.planet,
            'colonize': self.colonize,
            'systems': self.systems,
            'game': self.game,
            'next-turn': self.next_turn,
            'help': self.show_help,
            'clear': self.clear_screen,
            'exit': self.exit_cli
        }
        self.session = PromptSession()
        self.completer = WordCompleter(list(self.commands.keys()) + ['--format', 'json', 'table'])
        self.running = True

    def clear_screen(self, *args):
        """Clear the terminal screen."""
        clear()

    def exit_cli(self, *args):
        """Exit the CLI."""
        self.running = False
        console.print("[yellow]Goodbye![/yellow]")

    def show_help(self, *args):
        """Show help information."""
        help_table = Table(title="Available Commands")
        help_table.add_column("Command", style="cyan")
        help_table.add_column("Description", style="green")
        help_table.add_column("Usage", style="yellow")

        commands_help = {
            'player': ('Get player details', 'player <name> [--format json/table]'),
            'planet': ('Get planet details', 'planet <id> [--format json/table]'),
            'colonize': ('Colonize a planet', 'colonize <planet_id> <player_name>'),
            'systems': ('List star systems', 'systems [skip] [limit] [--format json/table]'),
            'game': ('Get game state', 'game <id> [--format json/table]'),
            'next-turn': ('Advance game turn', 'next-turn <game_id>'),
            'help': ('Show this help', 'help'),
            'clear': ('Clear screen', 'clear'),
            'exit': ('Exit the CLI', 'exit')
        }

        for cmd, (desc, usage) in commands_help.items():
            help_table.add_row(cmd, desc, usage)

        console.print(help_table)

    def parse_args(self, command_line: str) -> tuple[str, List[str], dict]:
        """Parse command line into command, args, and kwargs."""
        parts = command_line.split()
        if not parts:
            return '', [], {}

        command = parts[0]
        args = []
        kwargs = {}
        i = 1

        while i < len(parts):
            if parts[i].startswith('--'):
                key = parts[i][2:]
                if i + 1 < len(parts):
                    kwargs[key] = parts[i + 1]
                    i += 2
                else:
                    kwargs[key] = True
                    i += 1
            else:
                args.append(parts[i])
                i += 1

        return command, args, kwargs

    def player(self, *args, **kwargs):
        """Get player details by name."""
        if not args:
            console.print("[red]Error: Player name required[/red]")
            return

        format_type = Format(kwargs.get('format', 'table'))
        name = args[0]
        
        try:
            with httpx.Client() as client:
                response = client.get(f"{get_api_url()}/players/{name}")
                response.raise_for_status()
                data = response.json()
                
                if format_type == Format.json:
                    rprint(data)
                else:
                    player_table = Table(title=f"Player: {data['name']}")
                    player_table.add_column("Attribute", style="cyan")
                    player_table.add_column("Value", style="green")
                    
                    player_table.add_row("Empire", data['empire'])
                    
                    for resource, value in data['resources'].items():
                        player_table.add_row(f"Resource: {resource}", str(value))
                    
                    console.print(player_table)
        except httpx.HTTPError as e:
            console.print(f"[red]Error: {str(e)}[/red]")

    def planet(self, *args, **kwargs):
        """Get planet details by ID."""
        if not args:
            console.print("[red]Error: Planet ID required[/red]")
            return

        format_type = Format(kwargs.get('format', 'table'))
        planet_id = args[0]
        
        try:
            with httpx.Client() as client:
                response = client.get(f"{get_api_url()}/planets/{planet_id}")
                response.raise_for_status()
                data = response.json()
                
                if format_type == Format.json:
                    rprint(data)
                else:
                    planet_table = Table(title=f"Planet: {data['name']}")
                    planet_table.add_column("Attribute", style="cyan")
                    planet_table.add_column("Value", style="green")
                    
                    planet_table.add_row("ID", data['id'])
                    planet_table.add_row("Type", data['type'])
                    planet_table.add_row("Size", str(data['size']))
                    planet_table.add_row("Colonized", str(data['colonized']))
                    if data.get('owner'):
                        planet_table.add_row("Owner", data['owner'])
                    
                    if 'resources' in data:
                        for resource, value in data['resources'].items():
                            planet_table.add_row(f"Resource: {resource}", str(value))
                    
                    console.print(planet_table)
        except httpx.HTTPError as e:
            console.print(f"[red]Error: {str(e)}[/red]")

    def colonize(self, *args, **kwargs):
        """Colonize a planet."""
        if len(args) < 2:
            console.print("[red]Error: Planet ID and player name required[/red]")
            return

        planet_id, player_name = args[0], args[1]
        
        try:
            with httpx.Client() as client:
                response = client.patch(
                    f"{get_api_url()}/planets/{planet_id}/colonize",
                    params={"player_name": player_name}
                )
                response.raise_for_status()
                data = response.json()
                
                console.print(Panel(
                    f"[green]Successfully colonized planet {data['name']} for player {player_name}[/green]"
                ))
        except httpx.HTTPError as e:
            console.print(f"[red]Error: {str(e)}[/red]")

    def systems(self, *args, **kwargs):
        """List star systems."""
        skip = int(args[0]) if args else 0
        limit = int(args[1]) if len(args) > 1 else 10
        format_type = Format(kwargs.get('format', 'table'))
        
        try:
            with httpx.Client() as client:
                response = client.get(f"{get_api_url()}/systems/", params={"skip": skip, "limit": limit})
                response.raise_for_status()
                data = response.json()
                
                if format_type == Format.json:
                    rprint(data)
                else:
                    systems_table = Table(title="Star Systems")
                    systems_table.add_column("ID", style="cyan")
                    systems_table.add_column("Name", style="green")
                    systems_table.add_column("Position", style="magenta")
                    systems_table.add_column("Explored", style="yellow")
                    systems_table.add_column("Planets", style="blue")
                    
                    for system in data:
                        systems_table.add_row(
                            system['id'],
                            system['name'],
                            f"({system['position']['x']:.2f}, {system['position']['y']:.2f})",
                            "✓" if system['explored'] else "✗",
                            str(len(system.get('planets', [])))
                        )
                    
                    console.print(systems_table)
        except httpx.HTTPError as e:
            console.print(f"[red]Error: {str(e)}[/red]")

    def game(self, *args, **kwargs):
        """Get game state by ID."""
        if not args:
            console.print("[red]Error: Game ID required[/red]")
            return

        format_type = Format(kwargs.get('format', 'table'))
        game_id = args[0]
        
        try:
            with httpx.Client() as client:
                response = client.get(f"{get_api_url()}/games/{game_id}")
                response.raise_for_status()
                data = response.json()
                
                if format_type == Format.json:
                    rprint(data)
                else:
                    game_table = Table(title=f"Game State: {game_id}")
                    game_table.add_column("Attribute", style="cyan")
                    game_table.add_column("Value", style="green")
                    
                    game_table.add_row("Turn", str(data['turn']))
                    game_table.add_row("Difficulty", data['difficulty'])
                    game_table.add_row("Player Name", data['player']['name'])
                    game_table.add_row("Empire", data['player']['empire'])
                    
                    for resource, value in data['player']['resources'].items():
                        game_table.add_row(f"Resource: {resource}", str(value))
                    
                    game_table.add_row("Galaxy Size", data['galaxy']['size'])
                    game_table.add_row("Systems Count", str(data['galaxy']['systems']))
                    game_table.add_row("Explored Systems", str(data['galaxy']['explored']))
                    
                    console.print(game_table)
        except httpx.HTTPError as e:
            console.print(f"[red]Error: {str(e)}[/red]")

    def next_turn(self, *args, **kwargs):
        """Advance to the next turn."""
        if not args:
            console.print("[red]Error: Game ID required[/red]")
            return

        game_id = args[0]
        
        try:
            with httpx.Client() as client:
                response = client.patch(f"{get_api_url()}/games/{game_id}/turn")
                response.raise_for_status()
                data = response.json()
                
                console.print(Panel(
                    f"[green]Advanced to turn {data['turn']}[/green]"
                ))
        except httpx.HTTPError as e:
            console.print(f"[red]Error: {str(e)}[/red]")

    def run(self):
        """Run the interactive CLI."""
        console.print("[bold blue]Welcome to the 4X Space Empire Game CLI![/bold blue]")
        console.print("Type [green]help[/green] for available commands or [red]exit[/red] to quit.")
        
        while self.running:
            try:
                command_line = self.session.prompt(
                    HTML('<ansiyellow>4X-CLI></ansiyellow> '),
                    completer=self.completer
                )
                
                command, args, kwargs = self.parse_args(command_line)
                
                if command in self.commands:
                    self.commands[command](*args, **kwargs)
                elif command:
                    console.print(f"[red]Unknown command: {command}[/red]")
                    console.print("Type [green]help[/green] for available commands.")
            
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
            except Exception as e:
                console.print(f"[red]Error: {str(e)}[/red]")

def main():
    """Main entry point for the CLI."""
    cli = InteractiveCLI()
    cli.run()

if __name__ == "__main__":
    main() 