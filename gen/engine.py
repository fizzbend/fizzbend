import random
from models import World, Event, Faction

class SimulationEngine:
    def __init__(self, world: World):
        self.world = world

    def advance_year(self):
        """Advances the world by exactly one year and generates events."""
        self.world.year += 1
        yearly_events = []

        # 1. The Global Pulse (Constants and Volatiles Drift)
        self._apply_variable_drift()

        # 2. The Faction Turn (Geopolitics & Expansion)
        faction_events = self._process_factions()
        yearly_events.extend(faction_events)

        # 3. The Hero's Journey (Individual Actions - Placeholder for now)
        # We will hook this up when we build the Lexicon/Names
        
        # 4. Finalize the Ledger
        self._compile_ledger(yearly_events)

    def _apply_variable_drift(self):
        """Handles the 'Rubber Band' logic for world variables."""
        # Low-Flux (Constants) - Max 2% drift
        self.world.magic_level += random.randint(-2, 2)
        
        # High-Flux (Volatiles) - Max 10% drift normally, but kept within bounds
        self.world.stability += random.randint(-10, 10)
        
        # Clamp variables between 0 and 100 to prevent math breaking
        self.world.magic_level = max(0, min(100, self.world.magic_level))
        self.world.stability = max(0, min(100, self.world.stability))
        self.world.tech_level = max(0, min(100, self.world.tech_level))

    def _process_factions(self):
        """Iterates through active factions to determine their actions this year."""
        events = []
        factions = list(self.world.factions.values())
        
        for faction in factions:
            # Base growth
            if faction.is_majority:
                faction.local_tech += random.randint(1, 3)
            else:
                faction.local_tech += random.randint(0, 1)

            # Trigger Logic: Low Stability = Higher Chance of Conflict
            conflict_threshold = 30 + (100 - self.world.stability) # More unstable = higher threshold
            roll = random.randint(1, 100)

            if roll < (conflict_threshold * 0.2): # 20% of the threshold chance
                # Faction does something drastic!
                impact = {"stability": -5}
                
                # We will eventually pull the text below from lexicon.py
                title = f"{faction.race_name} Uprising"
                desc = f"The {faction.race_name} grew restless in year {self.world.year}, sparking a minor conflict that shook local trade."
                
                new_event = Event(
                    year=self.world.year,
                    title=title,
                    description=desc,
                    impact_vars=impact
                )
                new_event.involved_entities.append(faction.id)
                events.append(new_event)

        return events

    def _compile_ledger(self, events):
        """Saves the generated events to the world's memory."""
        # If nothing major happened, generate a 'Quiet Year' event
        if not events:
            quiet_event = Event(
                year=self.world.year,
                title="An Era of Quiet",
                description="The world turned, seasons changed, and the factions focused on survival rather than conquest.",
                impact_vars={"stability": +2} # Peace increases stability slightly
            )
            events.append(quiet_event)
            
        self.world.history_log.extend(events)