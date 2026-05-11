import google.generativeai as genai

class AIScribe:
    def __init__(self, api_key: str):
        # Configure the API connection
        genai.configure(api_key=api_key)
        
        # We use Flash because it is lightning fast and perfect for short text generation
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def chronicle_event(self, year: int, event_type: str, context: dict, stability: int) -> str:
        """
        Takes raw data from the engine and asks the AI to write a historical entry.
        """
        # Determine the tone based on the world's stability
        tone = "grim, chaotic, and brutal" if stability < 40 else "legendary, stoic, and historical"
        if stability > 70:
            tone = "prosperous, peaceful, and optimistic"

        # Construct the Prompt for the AI
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
        
        try:
            # Send the prompt to Gemini and get the text back
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            # A fallback just in case the internet cuts out or API rate limits hit
            return f"The records for Year {year} were lost to the ages. (Error: {e})"
