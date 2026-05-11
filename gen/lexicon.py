import random

# ==========================================
# 1. THE NAMING MATRICES
# ==========================================
NAMES = {
    "Dwarves": {
        "prefixes": ["Thrum", "Gorr", "Khaz", "Brak", "Urist", "Dorn"],
        "suffixes": ["-Hul", "-Ock", "son", "forge", "beard", "-Kar"]
    },
    "Elves": {
        "prefixes": ["Ael", "Sill", "Fae", "Leth", "Ves", "Gala"],
        "suffixes": ["yth", "ria", "dor", "wyn", "thil", "arion"]
    },
    "Tripki": {
        "prefixes": ["Grib", "Bog", "Cro", "Slit", "Bub", "Plop"],
        "suffixes": ["-Grib", "-Gobb", "ulo", "ik", "ak", "og"]
    },
    "Mutants": {
        "prefixes": ["X-", "Scab", "Rust", "Void", "Null", "Gore"],
        "suffixes": ["44", "king", "jaw", "born", "husk", "nine"]
    },
    "Humans": {
         "prefixes": ["Ed", "Art", "Leo", "Gwen", "Mar", "Tob"],
         "suffixes": ["ward", "hur", "idas", "dolyn", "cus", "ias"]
    }
}

# Fallback for races not yet fully defined
DEFAULT_NAMES = ["Brog", "Snark", "Zel", "Farn", "Kril", "Voss"]

# ==========================================
# 2. THE RELIC FORGE
# ==========================================
RELIC_COMPONENTS = {
    "prefixes": {
        "High_Magic": ["The Pulsing", "The Astral", "The Soul-Bound", "The Whispering"],
        "High_Tech": ["The Calibrated", "The Clockwork", "The Aether-Powered", "The Brass"],
        "Mundane": ["The Jagged", "The Blood-Stained", "The Ancient", "The Rusted"]
    },
    "objects": ["Eye", "Blade", "Chronometer", "Codex", "Crown", "Engine", "Root"],
    "suffixes": ["of the Void", "of the First King", "of the Deep", "that Weeps", "of Gears"]
}

# ==========================================
# 3. EVENT TEMPLATES (The "Mad Libs")
# ==========================================
EVENT_TEMPLATES = {
    "Conflict": [
        "The {faction_a} warbands clashed with the {faction_b} over control of the borderlands.",
        "Generational tensions boiled over as the {faction_a} razed several {faction_b} outposts.",
        "A swift and brutal campaign was launched by the {faction_a} against the unsuspecting {faction_b}."
    ],
    "Creation": [
        "In the quiet of the night, {creator_name} finished their life's work: {relic_name}.",
        "{creator_name}, driven by strange visions, forged {relic_name} from the bones of the earth.",
        "The world shifted slightly as {relic_name} was brought into existence by {creator_name}."
    ],
    "Expansion": [
        "Driven by population booms, the {faction_a} expanded their territory into the wilds.",
        "New trade routes were paved as the {faction_a} founded a new settlement.",
        "The {faction_a} spread their influence, building new spires and deep burrows."
    ]
}

# ==========================================
# 4. THE PARSER (The Tool to put it together)
# ==========================================
class LexiconParser:
    @staticmethod
    def generate_name(race: str) -> str:
        """Assembles a name based on the race's phonetic rules."""
        if race in NAMES:
            pool = NAMES[race]
            return random.choice(pool["prefixes"]) + random.choice(pool["suffixes"])
        else:
            return random.choice(DEFAULT_NAMES) + "-" + random.choice(DEFAULT_NAMES)

    @staticmethod
    def generate_relic_name(magic_level: int, tech_level: int) -> str:
        """Creates an item name influenced by the world's current state."""
        if magic_level > 70:
            prefix = random.choice(RELIC_COMPONENTS["prefixes"]["High_Magic"])
        elif tech_level > 70:
            prefix = random.choice(RELIC_COMPONENTS["prefixes"]["High_Tech"])
        else:
            prefix = random.choice(RELIC_COMPONENTS["prefixes"]["Mundane"])
            
        obj = random.choice(RELIC_COMPONENTS["objects"])
        suffix = random.choice(RELIC_COMPONENTS["suffixes"])
        
        return f"{prefix} {obj} {suffix}"

    @staticmethod
    def get_event_text(category: str, **kwargs) -> str:
        """Pulls a template and fills in the blanks with the provided arguments."""
        if category in EVENT_TEMPLATES:
            template = random.choice(EVENT_TEMPLATES[category])
            # The **kwargs lets us pass in faction_a="Dwarves", creator_name="Urist", etc.
            return template.format(**kwargs)
        return "An event lost to the sands of time."