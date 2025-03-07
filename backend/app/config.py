import json
import os
import enum
from pathlib import Path
from typing import Dict, List, Any, Type

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Path to the enums.json file
# Check if we're in Docker (where the config is mounted at /config)
if os.path.exists("/config"):
    ENUMS_FILE = Path("/config") / "enums.json"
else:
    ENUMS_FILE = PROJECT_ROOT / "config" / "enums.json"

# Load the enums from the JSON file
def load_enums() -> Dict[str, List[str]]:
    """Load enums from the JSON file."""
    try:
        with open(ENUMS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Enums file not found at {ENUMS_FILE}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in enums file at {ENUMS_FILE}")

# Create Enum classes dynamically
def create_enum_class(name: str, values: List[str]) -> Type[enum.Enum]:
    """Create an Enum class dynamically from a list of values."""
    return enum.Enum(name, {value.upper(): value for value in values})

# Load the enums
enums_data = load_enums()

# Create Enum classes
PlanetType = create_enum_class("PlanetType", enums_data["PlanetType"])
GalaxySize = create_enum_class("GalaxySize", enums_data["GalaxySize"])
Difficulty = create_enum_class("Difficulty", enums_data["Difficulty"])

# Export the Enum classes
__all__ = ["PlanetType", "GalaxySize", "Difficulty"]
