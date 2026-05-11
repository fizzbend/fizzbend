import uuid
from typing import List, Dict, Optional, Any

class Relic:
    """Represents a unique artifact or item of power."""
    def __init__(self, name: str, material: str, creator_id: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.material = material
        self.creator_id = creator_id
        self.current_owner_id: Optional[str] = None
        self.location_id: Optional[str] = None
        self.history: List[str] = [] # Tracks major events involving the relic

class Person:
    """Represents a historical actor (Hero, Villain, Craftsman)."""
    def __init__(self, name: str, race: str, role: str, home_city_id: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.race = race
        self.role = role
        self.is_alive = True
        self.home_city_id = home_city_id
        self.inventory: List[str] = [] # List of Relic IDs
        self.achievements: List[str] = []

class Settlement:
    """Represents a City, Landmark, or Ruin."""
    def __init__(self, name: str, primary_race: str, location_type: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.primary_race = primary_race
        self.location_type = location_type
        self.prosperity = 50
        self.is_ruined = False
        self.description = ""
        self.notable_relics: List[str] = [] # List of Relic IDs

class Faction:
    """Represents the geopolitical entity of a specific Ancestry."""
    def __init__(self, race_name: str, is_majority: bool = False):
        self.id = str(uuid.uuid4())
        self.race_name = race_name
        self.is_majority = is_majority
        self.population = 1000 if is_majority else 100
        self.local_tech = 10
        self.wealth = 50
        self.diplomacy: Dict[str, int] = {} # {other_faction_id: relationship_score (-100 to 100)}
        self.traits: List[str] = []
        self.dominant_belief: str = "Animism"

class Event:
    """The Ledger entry for a historical occurrence."""
    def __init__(self, year: int, title: str, description: str, impact_vars: Dict[str, int]):
        self.id = str(uuid.uuid4())
        self.year = year
        self.title = title
        self.description = description
        self.impact_vars = impact_vars # e.g., {"stability": -10, "tech": 5}
        self.involved_entities: List[str] = [] # List of UUIDs (People, Factions, Settlements)

class World:
    """The God Object: Holds all constants, volatiles, and entities."""
    def __init__(self, seed: str, majority_ancestry: str, active_minorities: List[str]):
        # Identifiers
        self.id = str(uuid.uuid4())
        self.seed = seed
        self.year = 0
        
        # Core Parameters (The Constants & Volatiles)
        self.stability = 50
        self.magic_level = 50
        self.tech_level = 10
        self.climate = "Temperate"
        self.size = "Medium"
        self.external_pressure = 10
        self.cultural_tone = "Neutral"
        
        # Entity Databases (Dictionaries keyed by UUID for fast lookup)
        self.factions: Dict[str, Faction] = {}
        self.settlements: Dict[str, Settlement] = {}
        self.people: Dict[str, Person] = {}
        self.relics: Dict[str, Relic] = {}
        self.history_log: List[Event] = []
        
        # Setup Initial Factions
        self._initialize_factions(majority_ancestry, active_minorities)

    def _initialize_factions(self, majority: str, minorities: List[str]):
        """Internal helper to bootstrap the active races on creation."""
        # Create Majority
        maj_faction = Faction(race_name=majority, is_majority=True)
        self.factions[maj_faction.id] = maj_faction
        
        # Create Minorities
        for race in minorities:
            if race != majority:
                min_faction = Faction(race_name=race, is_majority=False)
                self.factions[min_faction.id] = min_faction

    def get_faction_by_name(self, race_name: str) -> Optional[Faction]:
        """Helper method to easily find a faction without knowing its ID."""
        for faction in self.factions.values():
            if faction.race_name == race_name:
                return faction
        return None