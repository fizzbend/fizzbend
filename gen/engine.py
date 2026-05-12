def _process_factions(self):
        """Iterates through factions to determine what happens, but does NOT write the text yet."""
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

                # Save the raw data for the AI to read later
                raw_event_data = f"The {faction.race_name} engaged in a {event_type}."
                raw_yearly_events.append(raw_event_data)

        return raw_yearly_events

    def _compile_ledger(self, raw_events):
        """Takes all the raw data for the year and asks the AI to write ONE master entry."""
        if not raw_events:
            raw_events = ["A completely peaceful, uneventful year of recovery and changing seasons."]
            self.world.stability += 2 # Peace heals stability
            title = "An Era of Quiet"
        else:
            title = f"The Events of Year {self.world.year}"

        # --- THE AI WRITER (Only called ONCE per year now) ---
        if self.ai_scribe:
            desc = self.ai_scribe.chronicle_year(
                year=self.world.year,
                events_list=raw_events,
                stability=self.world.stability
            )
        else:
            # Fallback if AI is offline
            desc = f"In year {self.world.year}, the following occurred: " + " ".join(raw_events)

        # Create one master Event card for the UI
        master_event = Event(
            year=self.world.year,
            title=title,
            description=desc,
            impact_vars={"Events": len(raw_events)}
        )
            
        self.world.history_log.append(master_event)
