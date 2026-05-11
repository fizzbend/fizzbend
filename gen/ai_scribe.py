import google.generativeai as genai
import time # <-- We need this to make the app pause

class AIScribe:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def chronicle_event(self, year: int, event_type: str, context: dict, stability: int) -> str:
        tone = "grim, chaotic, and brutal" if stability < 40 else "legendary, stoic, and historical"
        if stability > 70:
            tone = "prosperous, peaceful, and optimistic"

        prompt = f"""
        You are the 'Fizzbend Historian', a neutral but vivid chronicler of a fantasy world.
        Write a 2-to-3 sentence historical ledger entry for Year {year}.
        
        Event Details: 
        - Type of Event: {event_type}
        - Entities Involved: {context}
        
        Guidelines:
        - The current world stability is {stability}/100. The tone of your writing must be: {tone}.
        - Do not use flowery, overly poetic language. Write like a gritty, realistic history book.
        - NEVER start with "In Year {year}...". Jump straight into the action.
        - Do not add conversational filler. Output ONLY the historical text.
        """
        
        # --- THE RETRY LOOP ---
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                error_msg = str(e)
                # If it's a rate limit error, wait and retry
                if "429" in error_msg:
                    time.sleep(10) # Pause for 10 seconds to let the quota reset
                    continue # Try again!
                else:
                    return f"The records for Year {year} were lost. (Error: {e})"
        
        return f"The records for Year {year} were heavily fragmented due to the Historian needing a break."
