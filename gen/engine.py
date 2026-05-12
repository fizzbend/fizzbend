import random
from models import World, Event, Faction

class SimulationEngine:
    def __init__(self, world: World, ai_scribe=None):
        """
        Initializes the engine. 
        ai_scribe is an optional instance of the AIScribe class. 
        """
        self.world = world
        self.ai_scribe = ai_scribe 

    def advance_year(self):
        """Advances the world by exactly one year and generates events."""
        self.world.year += 1

        # 1. The Global Pulse (Constants and Volatiles Drift)
        self._apply_variable_drift()

        # 2. The Faction Turn (Geopolitics & Expansion)
        raw_events = self._process_factions()
        
        # 3. Finalize the Ledger (Send to AI)
        self._compile_ledger(raw_events)

    def _apply_variable_drift(self):
        """Handles the 'Rubber Band' logic for world variables."""
        self.world.magic_level += random.randint(-2, 2)
        self.world.stability += random.randint(-10, 10)
        
        # Clamp variables between 0 and 100
        self.world.magic_level = max(0, min(100, self.world.magic_level))
        self.world.stability = max(0, min(100, self.world.stability))
        self.world.tech_level = max(0, min(100, self.world.tech_level))

    def _process_factions(self):
        """Iterates through factions to determine what happens (Math only)."""
        raw_yearly_events = []
        factions = list(self.world.factions.values())
        
        for faction in factions:
            if faction.is_majority:
                faction.local_tech += random.randint(1, 3)
            else:
                faction.local_tech += random.randint(0, 1)

            conflict_threshold = 30 + (100 - self.world.stability)
            roll = random.randint(1, 100)

            if roll < (conflict_threshold * 0.2):
                if self.world.stability < 40:
                    event_type = "Violent Skirmish or Uprising"
                    self.world.stability -= 5
                elif faction.local_tech > 50:
                    event_type = "Technological Breakthrough"
                    faction.local_tech += 5
                else:
                    event_type = "Border Dispute"
                    self.world.stability -= 2

                raw_event_data = f"The {faction.race_name} engaged in a {event_type}."
                raw_yearly_events.append(raw_event_data)

        return raw_yearly_events

    def _compile_ledger(self, raw_events):
        """Takes all the raw data for the year and asks the AI to write ONE master entry."""
        if not raw_events:
            raw_events = ["A completely peaceful, uneventful year of recovery and changing seasons."]
            self.world.stability += 2 
            title = "An Era of Quiet"
        else:
            title = f"The Events of Year {self.world.year}"

        # --- THE AI WRITER ---
        if self.ai_scribe:
            desc = self.ai_scribe.chronicle_year(
                year=self.world.year,
                events_list=raw_events,
                stability=self.world.stability
            )
        else:
            desc = f"In year {self.world.year}, the following occurred: " + " ".join(raw_events)

        master_event = Event(
            year=self.world.year,
            title=title,
            description=desc,
            impact_vars={"Events": len(raw_events)}
        )
            
        self.world.history_log.append(master_event)
