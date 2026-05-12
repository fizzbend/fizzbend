import google.generativeai as genai
import time 

class AIScribe:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def chronicle_year(self, year: int, events_list: list, stability: int) -> str:
        """
        Takes a list of ALL events that happened this year and writes a single cohesive summary.
        """
        tone = "grim, chaotic, and brutal" if stability < 40 else "legendary, stoic, and historical"
        if stability > 70:
            tone = "prosperous, peaceful, and optimistic"

        # Format the raw events into a readable list for the AI
        raw_data = "\n".join([f"- {e}" for e in events_list])

        prompt = f"""
        You are the 'Fizzbend Historian', chronicling a fantasy world.
        Below is raw data of everything that occurred in Year {year}. 
        
        Raw Data: 
        {raw_data}
        
        Guidelines:
        - Write a cohesive 3-to-4 sentence historical summary of this year.
        - Weave these separate events together into a narrative if possible.
        - The current world stability is {stability}/100. The tone must be: {tone}.
        - Do not use flowery, poetic language. Keep it grounded and historical.
        - Output ONLY the historical text. Do not include bullet points.
        """
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                # Add a mandatory 2-second cooldown to pace the Free Tier limit
                time.sleep(2) 
                return response.text.strip()
            except Exception as e:
                if "429" in str(e):
                    time.sleep(10) # Pause and retry
                    continue
                else:
                    return f"The records for Year {year} were lost. (Error: {e})"
        
        return f"The records for Year {year} were heavily fragmented due to missing archives."
