import random
from models import World, Event, Faction

class SimulationEngine:
    def __init__(self, world: World, ai_scribe=None):
        """
        Initializes the engine. 
        ai_scribe is an optional instance of the AIScribe class. 
        If provided, the AI writes the history. If None, it uses static text.
        """
        self.world = world
        self.ai_scribe = ai_scribe 

    def advance_year(self):
        """Advances the world by exactly one year and generates events."""
        self.world.year += 1
        yearly_events = []

        # 1. The Global Pulse (Constants and Volatiles Drift)
        self._apply_variable_drift()

        # 2. The Faction Turn (Geopolitics & Expansion)
        faction_events = self._process_factions()
        yearly_events.extend(faction_events)
        
        # 3. Finalize the Ledger
        self._compile_ledger(yearly_events)

    def _apply_variable_drift(self):
        """Handles the 'Rubber Band' logic for world variables."""
        # Low-Flux (Constants) - Max 2% drift
        self.world.magic_level += random.randint(-2, 2)
        
        # High-Flux (Volatiles) - Max 10% drift normally
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
            # Base technological growth
            if faction.is_majority:
                faction.local_tech += random.randint(1, 3)
            else:
                faction.local_tech += random.randint(0, 1)

            # Trigger Logic: Low Stability = Higher Chance of Conflict
            conflict_threshold = 30 + (100 - self.world.stability)
            roll = random.randint(1, 100)

            # If the roll is under 20% of the threshold, an event occurs!
            if roll < (conflict_threshold * 0.2):
                
                # Determine the TYPE of event based on the faction's state
                if self.world.stability < 40:
                    event_type = "Violent Skirmish or Uprising"
                    impact = {"stability": -5, "tech": -1}
                    title = f"The {faction.race_name} Conflict"
                elif faction.local_tech > 50:
                    event_type = "Technological Breakthrough or Expansion"
                    impact = {"stability": -2, "tech": +5}
                    title = f"{faction.race_name} Innovation"
                else:
                    event_type = "Border Dispute or Cultural Shift"
                    impact = {"stability": -3}
                    title = f"The {faction.race_name} Incident"

                # Build the context dictionary to feed to the AI
                event_context = {
                    "Actor": faction.race_name,
                    "Faction Tech Level": faction.local_tech,
                    "World Magic Level": self.world.magic_level,
                    "Climate": self.world.climate
                }

                # --- THE AI WRITER ---
                if self.ai_scribe:
                    # Ask Gemini to write the event
                    desc = self.ai_scribe.chronicle_event(
                        year=self.world.year,
                        event_type=event_type,
                        context=event_context,
                        stability=self.world.stability
                    )
                else:
                    # Safety Fallback if AI is offline
                    desc = f"In year {self.world.year}, a notable {event_type.lower()} involved the {faction.race_name}."

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
        """Saves the generated events to the world's memory. Handles peaceful years."""
        if not events:
            # Even for quiet years, we can let the AI paint a beautiful picture of peace
            if self.ai_scribe:
                desc = self.ai_scribe.chronicle_event(
                    year=self.world.year,
                    event_type="A completely peaceful, uneventful year of recovery.",
                    context={"Atmosphere": "Quiet, recovering, changing seasons."},
                    stability=self.world.stability
                )
            else:
                desc = "The world turned, seasons changed, and the factions focused on survival rather than conquest."

            quiet_event = Event(
                year=self.world.year,
                title="An Era of Quiet",
                description=desc,
                impact_vars={"stability": +2} # Peace heals stability
            )
            events.append(quiet_event)
            
        self.world.history_log.extend(events)