import random

# Lists for name generation
PREFIXES = [
    "Stellar", "Galactic", "Cosmic", "Astral", "Celestial",
    "Imperial", "Ancient", "Eternal", "Grand", "Supreme",
    "United", "Federated", "Allied", "Sovereign", "Royal"
]

CORE_NAMES = [
    "Empire", "Federation", "Alliance", "Dominion", "Republic",
    "Collective", "Hegemony", "Dynasty", "Consortium", "Union",
    "Commonwealth", "Confederation", "Imperium", "Assembly", "Council"
]

SUFFIXES = [
    "of the Stars", "of the Core Worlds", "of the Rim", "of the Void",
    "of the Galaxy", "of the Nebula", "of the Cluster", "of Light",
    "of Unity", "of Power", "of Harmony", "of Order", "of Progress",
    "of Enlightenment", "of Destiny"
]

SPECIES_NAMES = [
    "Zylaxian", "Thorian", "Veldari", "Nexari", "Kryloth",
    "Aetherian", "Draknid", "Sylvoid", "Quanton", "Meridian",
    "Helixian", "Vortan", "Xylith", "Centari", "Proximan"
]

def generate_empire_name() -> str:
    """Generate a random empire name."""
    name_type = random.choice([
        "standard",  # e.g. "Stellar Empire of the Stars"
        "species",   # e.g. "Zylaxian Collective"
        "simple"     # e.g. "Grand Federation"
    ])
    
    if name_type == "standard":
        return f"{random.choice(PREFIXES)} {random.choice(CORE_NAMES)} {random.choice(SUFFIXES)}"
    elif name_type == "species":
        return f"{random.choice(SPECIES_NAMES)} {random.choice(CORE_NAMES)}"
    else:  # simple
        return f"{random.choice(PREFIXES)} {random.choice(CORE_NAMES)}"

def generate_system_name() -> str:
    """Generate a random star system name."""
    # Implementation for system names (to be added later)
    pass 