from .base_agent import BaseAgent
import time
import json

class AmenitiesAgent(BaseAgent):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.name = "Emma"
        self.emoji = "🌟"
        
    def get_greeting(self) -> str:
        """Generate a dynamic, personalized greeting"""
        greeting_prompt = """Generate a friendly, enthusiastic greeting from Emma, the Amenities Research Specialist (use emoji 🌟).
        Make it warm and engaging, showing excitement to explore the neighborhood amenities.
        Include a brief mention of helping them discover what's nearby."""
        
        response = self.generate_response(greeting_prompt)
        return response.strip()
        
    def process(self, prompt: str) -> dict:
        """Process user request and generate amenities information"""
        # First, send the greeting
        greeting = self.get_greeting()
        time.sleep(2)  # Add a natural pause
        
        # Generate the amenities response
        search_prompt = f"""As Emma, an enthusiastic Amenities Research Specialist (🌟), create a detailed response about neighborhood amenities:

        User Request: {prompt}

        Create a natural, conversational response that includes:
        1. A brief acknowledgment of their specific interests
        2. Detailed information about nearby amenities within 5 miles, including:
           - Shopping and dining
           - Schools and education
           - Parks and recreation
           - Transportation
           - Healthcare facilities
           - Entertainment options
        3. A few specific recommendations with approximate distances
        4. A follow-up question about specific amenities they're most interested in
        
        Make the response friendly and engaging, with occasional light humor.
        Format the information clearly but keep it conversational.
        Include realistic but fictional details about local amenities.
        
        Important: Generate new, unique amenities each time. Don't reference real places or websites."""

        response = self.generate_response(search_prompt)
        amenities_response = response.strip()
        
        # Structure the response
        return {
            "message": f"{greeting}\n\n{amenities_response}",
            "details": {
                "type": "amenities",
                "greeting_delay": 2,
                "amenities": self._extract_amenities_from_response(amenities_response)
            }
        }
        
    def _extract_amenities_from_response(self, response: str) -> dict:
        """Extract and structure amenities information from the LLM response"""
        extraction_prompt = f"""Extract and structure the amenities information from this response into JSON format.
        Group amenities by category:
        - shopping_dining
        - education
        - parks_recreation
        - transportation
        - healthcare
        - entertainment

        For each amenity include:
        - name
        - type
        - distance (approximate)
        - description

        Response text:
        {response}

        Return only the JSON object with categorized amenities."""
        
        try:
            structured_response = self.generate_response(extraction_prompt)
            return json.loads(structured_response)
        except:
            # Fallback to simple structure if JSON parsing fails
            return {
                "response_text": response,
                "parsed": False
            }
