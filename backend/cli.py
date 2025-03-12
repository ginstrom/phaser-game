import typer
import httpx
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint
from typing import Optional, List, Dict
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
            'players': self.list_players,
            'planet': self.planet,
            'planets': self.list_planets,
            'colonize': self.colonize,
            'systems': self.list_systems,
            'system': self.system_details,
            'game': self.game,
            'new-game': self.new_game,
            'next-turn': self.next_turn,
            'help': self.show_help,
            'clear': self.clear_screen,
            'exit': self.exit_cli
        }
        self.session = PromptSession()
        self.completer = WordCompleter(list(self.commands.keys()) + ['--format', 'json', 'table'])
        self.running = True
        # Cache for system and planet data to support index-based access
        self.systems_cache: Dict[int, dict] = {}
        self.planets_cache: Dict[str, Dict[int, dict]] = {}  # system_id -> {index: planet_data}

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
            'players': ('List all players', 'players [--format json/table]'),
            'player': ('Get player details', 'player <name/index> [--format json/table]'),
            'planets': ('List planets in a system', 'planets <system_index> [--format json/table]'),
            'planet': ('Get planet details', 'planet <system_index> <planet_index> [--format json/table]'),
            'colonize': ('Colonize a planet', 'colonize <system_index> <planet_index> <player_name>'),
            'systems': ('List star systems', 'systems [--format json/table]'),
            'system': ('Get system details', 'system <index> [--format json/table]'),
            'game': ('Get game state', 'game <id> [--format json/table]'),
            'new-game': ('Create a new game', 'new-game <player_name> <empire_name>'),
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

    def list_players(self, *args, **kwargs):
        """List all players with indices."""
        format_type = Format(kwargs.get('format', 'table'))
        
        try:
            with httpx.Client() as client:
                response = client.get(f"{get_api_url()}/players/")
                response.raise_for_status()
                data = response.json()
                
                if format_type == Format.json:
                    rprint(data)
                else:
                    players_table = Table(title="Players")
                    players_table.add_column("Index", style="cyan")
                    players_table.add_column("Name", style="green")
                    players_table.add_column("Empire", style="yellow")
                    
                    for idx, player in enumerate(data):
                        players_table.add_row(
                            str(idx),
                            player['name'],
                            player['empire']
                        )
                    
                    console.print(players_table)
                    console.print("\nUse 'player <index>' to view details")
        except httpx.HTTPError as e:
            console.print(f"[red]Error: {str(e)}[/red]")

    def player(self, *args, **kwargs):
        """Get player details by name or index."""
        if not args:
            console.print("[red]Error: Player name or index required[/red]")
            return

        format_type = Format(kwargs.get('format', 'table'))
        player_id = args[0]
        
        try:
            with httpx.Client() as client:
                # First try to get all players to resolve index
                if player_id.isdigit():
                    list_response = client.get(f"{get_api_url()}/players/")
                    list_response.raise_for_status()
                    players = list_response.json()
                    if int(player_id) >= len(players):
                        console.print(f"[red]Error: Invalid player index {player_id}[/red]")
                        return
                    player_id = players[int(player_id)]['name']

                response = client.get(f"{get_api_url()}/players/{player_id}")
                response.raise_for_status()
                data = response.json()
                
                if format_type == Format.json:
                    rprint(data)
                else:
                    player_table = Table(title=f"Player: {data['name']}")
                    player_table.add_column("Attribute", style="cyan")
                    player_table.add_column("Value", style="green")
                    
                    player_table.add_row("Name", data['name'])
                    player_table.add_row("Empire", data['empire'])
                    
                    for resource, value in data['resources'].items():
                        player_table.add_row(f"Resource: {resource}", str(value))
                    
                    console.print(player_table)
        except httpx.HTTPError as e:
            console.print(f"[red]Error: {str(e)}[/red]")

    def list_systems(self, *args, **kwargs):
        """List star systems with indices."""
        format_type = Format(kwargs.get('format', 'table'))
        
        try:
            with httpx.Client() as client:
                response = client.get(f"{get_api_url()}/systems/")
                response.raise_for_status()
                data = response.json()
                
                # Update systems cache
                self.systems_cache = {i: system for i, system in enumerate(data)}
                
                if format_type == Format.json:
                    rprint(data)
                else:
                    systems_table = Table(title="Star Systems")
                    systems_table.add_column("Index", style="cyan")
                    systems_table.add_column("Name", style="green")
                    systems_table.add_column("Position", style="magenta")
                    systems_table.add_column("Explored", style="yellow")
                    systems_table.add_column("Planets", style="blue")
                    
                    for idx, system in self.systems_cache.items():
                        systems_table.add_row(
                            str(idx),
                            system['name'],
                            f"({system['position']['x']:.2f}, {system['position']['y']:.2f})",
                            "✓" if system['explored'] else "✗",
                            str(len(system.get('planets', [])))
                        )
                    
                    console.print(systems_table)
                    console.print("\nUse 'system <index>' to view details")
                    console.print("Use 'planets <index>' to list planets in a system")
        except httpx.HTTPError as e:
            console.print(f"[red]Error: {str(e)}[/red]")

    def system_details(self, *args, **kwargs):
        """Get system details by index."""
        if not args:
            console.print("[red]Error: System index required[/red]")
            return

        format_type = Format(kwargs.get('format', 'table'))
        try:
            system_idx = int(args[0])
            if system_idx not in self.systems_cache:
                console.print(f"[red]Error: Invalid system index {system_idx}[/red]")
                return
            
            system = self.systems_cache[system_idx]
            
            if format_type == Format.json:
                rprint(system)
            else:
                system_table = Table(title=f"System: {system['name']}")
                system_table.add_column("Attribute", style="cyan")
                system_table.add_column("Value", style="green")
                
                system_table.add_row("Index", str(system_idx))
                system_table.add_row("Name", system['name'])
                system_table.add_row("Position", f"({system['position']['x']:.2f}, {system['position']['y']:.2f})")
                system_table.add_row("Explored", "✓" if system['explored'] else "✗")
                system_table.add_row("Planets", str(len(system.get('planets', []))))
                
                console.print(system_table)
                console.print("\nUse 'planets <index>' to list planets in this system")
        except ValueError:
            console.print("[red]Error: System index must be a number[/red]")
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")

    def list_planets(self, *args, **kwargs):
        """List planets in a system by system index."""
        if not args:
            console.print("[red]Error: System index required[/red]")
            return

        format_type = Format(kwargs.get('format', 'table'))
        try:
            system_idx = int(args[0])
            if system_idx not in self.systems_cache:
                console.print(f"[red]Error: Invalid system index {system_idx}[/red]")
                return
            
            system = self.systems_cache[system_idx]
            planets = system.get('planets', [])
            
            # Update planets cache for this system
            self.planets_cache[str(system_idx)] = {i: planet for i, planet in enumerate(planets)}
            
            if format_type == Format.json:
                rprint(planets)
            else:
                planets_table = Table(title=f"Planets in {system['name']}")
                planets_table.add_column("Index", style="cyan")
                planets_table.add_column("Name", style="green")
                planets_table.add_column("Type", style="yellow")
                planets_table.add_column("Size", style="blue")
                planets_table.add_column("Colonized", style="magenta")
                planets_table.add_column("Owner", style="red")
                
                for idx, planet in self.planets_cache[str(system_idx)].items():
                    planets_table.add_row(
                        str(idx),
                        planet['name'],
                        planet['type'],
                        str(planet['size']),
                        "✓" if planet['colonized'] else "✗",
                        planet.get('owner', '-')
                    )
                
                console.print(planets_table)
                console.print("\nUse 'planet <system_index> <planet_index>' to view details")
        except ValueError:
            console.print("[red]Error: System index must be a number[/red]")
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")

    def planet(self, *args, **kwargs):
        """Get planet details by system and planet indices."""
        if len(args) < 2:
            console.print("[red]Error: Both system index and planet index required[/red]")
            return

        format_type = Format(kwargs.get('format', 'table'))
        try:
            system_idx = int(args[0])
            planet_idx = int(args[1])
            
            if system_idx not in self.systems_cache:
                console.print(f"[red]Error: Invalid system index {system_idx}[/red]")
                return
            
            if str(system_idx) not in self.planets_cache or planet_idx not in self.planets_cache[str(system_idx)]:
                # Load planets if not in cache
                self.list_planets([system_idx])
            
            if str(system_idx) not in self.planets_cache or planet_idx not in self.planets_cache[str(system_idx)]:
                console.print(f"[red]Error: Invalid planet index {planet_idx}[/red]")
                return
            
            planet = self.planets_cache[str(system_idx)][planet_idx]
            
            if format_type == Format.json:
                rprint(planet)
            else:
                planet_table = Table(title=f"Planet: {planet['name']}")
                planet_table.add_column("Attribute", style="cyan")
                planet_table.add_column("Value", style="green")
                
                planet_table.add_row("Name", planet['name'])
                planet_table.add_row("Type", planet['type'])
                planet_table.add_row("Size", str(planet['size']))
                planet_table.add_row("Colonized", "✓" if planet['colonized'] else "✗")
                if planet.get('owner'):
                    planet_table.add_row("Owner", planet['owner'])
                
                if 'resources' in planet:
                    for resource, value in planet['resources'].items():
                        planet_table.add_row(f"Resource: {resource}", str(value))
                
                console.print(planet_table)
        except ValueError:
            console.print("[red]Error: Both system index and planet index must be numbers[/red]")
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")

    def colonize(self, *args, **kwargs):
        """Colonize a planet using system index, planet index, and player name."""
        if len(args) < 3:
            console.print("[red]Error: System index, planet index, and player name required[/red]")
            return

        try:
            system_idx = int(args[0])
            planet_idx = int(args[1])
            player_name = args[2]
            
            if system_idx not in self.systems_cache:
                console.print(f"[red]Error: Invalid system index {system_idx}[/red]")
                return
            
            if str(system_idx) not in self.planets_cache or planet_idx not in self.planets_cache[str(system_idx)]:
                # Load planets if not in cache
                self.list_planets([system_idx])
            
            if str(system_idx) not in self.planets_cache or planet_idx not in self.planets_cache[str(system_idx)]:
                console.print(f"[red]Error: Invalid planet index {planet_idx}[/red]")
                return
            
            planet = self.planets_cache[str(system_idx)][planet_idx]
            
            with httpx.Client() as client:
                response = client.patch(
                    f"{get_api_url()}/planets/{planet['id']}/colonize",
                    params={"player_name": player_name}
                )
                response.raise_for_status()
                data = response.json()
                
                console.print(Panel(
                    f"[green]Successfully colonized planet {data['name']} for player {player_name}[/green]"
                ))
                
                # Update cache
                self.planets_cache[str(system_idx)][planet_idx] = data
        except ValueError:
            console.print("[red]Error: System index and planet index must be numbers[/red]")
        except httpx.HTTPError as e:
            console.print(f"[red]Error: {str(e)}[/red]")

    def new_game(self, *args, **kwargs):
        """Create a new game."""
        if len(args) < 2:
            console.print("[red]Error: Player name and empire name required[/red]")
            return
        
        player_name = args[0]
        empire_name = args[1]
        
        try:
            with httpx.Client() as client:
                response = client.post(
                    f"{get_api_url()}/games/",
                    json={
                        "player_name": player_name,
                        "empire_name": empire_name
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                console.print(Panel(
                    f"[green]Successfully created new game![/green]\n"
                    f"Game ID: {data['id']}\n"
                    f"Player: {data['player']['name']}\n"
                    f"Empire: {data['player']['empire']}\n"
                    f"Turn: {data['turn']}"
                ))
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