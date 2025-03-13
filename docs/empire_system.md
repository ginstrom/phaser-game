# Empire System Documentation

## Overview
The empire system manages civilizations within the game, including both player-controlled and AI empires. Each empire has its own characteristics, resources, and perks that influence gameplay.

## Core Components

### Empire Model
```python
class Empire:
    id: str                     # Unique identifier
    game_id: str               # Reference to parent game
    name: str                  # Empire name
    is_player: bool            # Whether this is a player empire
    color: str                 # Hex color code for empire
    credits: int              # Currency
    research_points: int      # Research currency
    research_levels: Dict     # Progress in different research areas
```

### Empire Perks
Each empire has four core attributes that affect their gameplay:
- `research_efficiency`: Affects research point generation and technology costs
- `combat_efficiency`: Affects military unit strength and combat outcomes
- `economic_efficiency`: Affects resource generation and trade
- `diplomatic_influence`: Affects relationships with other empires

### Resource System
Starting resources are difficulty-dependent:
```json
{
  "easy": {
    "credits": 2000,
    "research_points": 100
  },
  "normal": {
    "credits": 1000,
    "research_points": 50
  },
  "hard": {
    "credits": 500,
    "research_points": 25
  }
}
```

### Empire Archetypes
Pre-defined empire types for AI opponents:

1. **Militant**
   - Strong combat focus
   - Weaker in research and diplomacy
   - Uses red color scheme

2. **Scientific**
   - Strong research focus
   - Weaker in combat
   - Uses blue color scheme

3. **Economic**
   - Strong economic focus
   - Balanced other attributes
   - Uses gold color scheme

## Game Integration

### Empire Creation
Empires are created during game initialization through:
1. `create_player_empire()`: Creates the human player's empire
2. `create_computer_empire()`: Creates AI-controlled empires
3. `initialize_game_empires()`: Orchestrates creation of all empires for a game

### API Endpoints
- `POST /games`: Creates a new game with empires
  ```json
  {
    "player_name": string,
    "difficulty": string,
    "galaxy_size": string,
    "num_computer_empires": number?,
    "player_perks": object?
  }
  ```

## Configuration
Empire settings are managed through `game_config.json`, including:
- Default perks
- Starting resources by difficulty
- Empire archetypes
- Perk point allocation rules
- Game settings (min/max empires, etc.) 