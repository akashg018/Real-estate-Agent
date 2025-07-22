from .base_agent import BaseAgent

class LocationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Jack",
            personality="I'm Jack, your adventure-loving location guide! 📍 I'll turn your commutes into shortcuts!",
            emoji="📍",
            role="Transportation & Distance Expert"
        )

    def get_response(self, property_info):
        prompt = f"""
You are a location analysis expert.

For this property: {property_info}

Output JSON ONLY:

{{
    "key_distances": {{
        "university": "0.5 miles",
        "hospital": "2 miles",
        "supermarket": "0.3 miles"
    }},
    "transport_options": ["Bus", "Metro", "Bike"],
    "average_commute_time": "15 mins"
}}

Strictly respond in JSON format.
"""
        response_data = self._get_openai_response(prompt)
        print("📍 Raw LocationAgent Response:", response_data)

        return response_data if isinstance(response_data, dict) else {}
