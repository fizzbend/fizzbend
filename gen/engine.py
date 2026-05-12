import random
from models import World, Event, Faction

class SimulationEngine:
    def __init__(self, world: World, ai_scribe=None):
        self.world = world
        self.ai_scribe = ai_scribe 

    def advance_era(self, years_to_sim: int):
        """Advances the world by multiple years, then asks the AI to summarize the Era."""
        start_year = self.world.year + 1
        raw_era_events = []

        # Run the math silently for the requested number of years
        for _ in range(years_to_sim):
            self.world.year += 1
            self._apply_variable_drift()
            yearly_raw = self._process_factions()
            
            if yearly_raw:
                raw_era_events.append(f"Year {self.world.year}: " + " ".join(yearly_raw))
            else:
                raw_era_events.append(f"Year {self.world.year}: A quiet year of recovery.")

        end_year = self.world.year
        
        # Now that the math is done, compile the ledger ONCE
        self._compile_era_ledger(start_year, end_year, raw_era_events)

    def _apply_variable_drift(self):
        self.world.magic_level += random.randint(-2, 2)
        self.world.stability += random.randint(-10, 10)
        
        self.world.magic_level = max(0, min(100, self.world.magic_level))
        self.world.stability = max(0, min(100, self.world.stability))
        self.world.tech_level = max(0, min(100, self.world.tech_level))

    def _process_factions(self):
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

    def _compile_era_ledger(self, start_year, end_year, raw_events):
        """Asks the AI to write ONE master entry for the entire Era."""
        if start_year == end_year:
            title = f"The Events of Year {start_year}"
        else:
            title = f"The Era of {start_year} to {end_year}"

        if self.ai_scribe:
            desc = self.ai_scribe.chronicle_era(
                start_year=start_year,
                end_year=end_year,
                events_list=raw_events,
                stability=self.world.stability
            )
        else:
            desc = f"Between years {start_year} and {end_year}, the following occurred: " + " ".join(raw_events)

        master_event = Event(
            year=end_year,  # Attach to the final year of the era
            title=title,
            description=desc,
            impact_vars={"Years Covered": (end_year - start_year) + 1}
        )
            
        self.world.history_log.append(master_event)
