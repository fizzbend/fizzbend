import google.generativeai as genai
import time 

class AIScribe:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def chronicle_era(self, start_year: int, end_year: int, events_list: list, stability: int) -> str:
        """
        Takes a list of ALL events across multiple years and writes a sweeping Era summary.
        """
        tone = "grim, chaotic, and brutal" if stability < 40 else "legendary, stoic, and historical"
        if stability > 70:
            tone = "prosperous, peaceful, and optimistic"

        raw_data = "\n".join([f"- {e}" for e in events_list])

        prompt = f"""
        You are the 'Fizzbend Historian', chronicling a fantasy world.
        Below is the raw data of everything that occurred between Year {start_year} and Year {end_year}. 
        
        Raw Data: 
        {raw_data}
        
        Guidelines:
        - Write a cohesive 4-to-5 sentence historical summary of this Era.
        - Weave these separate yearly events together into a broader narrative or trend.
        - The current world stability at the end of this era is {stability}/100. The tone must be: {tone}.
        - Do not use flowery, poetic language. Keep it grounded and historical.
        - Output ONLY the historical text. Do not include bullet points.
        """
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                if "429" in str(e):
                    time.sleep(10) # Brief pause if we hit a random snag
                    continue
                else:
                    return f"The records for the Era of {start_year}-{end_year} were lost. (Error: {e})"
        
        return f"The archives from Year {start_year} to {end_year} were heavily fragmented."
