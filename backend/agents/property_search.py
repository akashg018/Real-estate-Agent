from .base_agent import BaseAgent
import time
import json

class PropertySearchAgent(BaseAgent):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.name = "Mike"
        self.emoji = "🏠"

    def get_greeting(self) -> str:
        """Generate a dynamic, personalized greeting"""
        greeting_prompt = """Generate a friendly, slightly humorous greeting from a real estate agent named Mike (use emoji 🏠).
        The greeting should be warm and welcoming, showing enthusiasm to help find the perfect property.
        Make it sound natural and conversational. Include a question about what they're looking for in a property."""
        
        response = self.generate_response(greeting_prompt)
        return response.strip()
        
    def process(self, prompt: str, context: dict = None) -> dict:
        """Process user request and generate property recommendations with context awareness"""
        # First, send the greeting
        greeting = self.get_greeting()
        time.sleep(2)  # Add a natural pause
        
        # Check context for existing properties
        existing_properties = []
        if context and "properties" in context:
            existing_properties = [
                f"Previously Discussed Property:\n"
                f"Name: {prop['name']}\n"
                f"Price: {prop['price']}\n"
                f"Location: {prop.get('location', 'Not specified')}\n"
                f"Features: {', '.join(prop.get('features', []))}\n"
                for prop in context["properties"]
            ]
        
        # Generate the property search response
        search_prompt = f"""As Mike, an enthusiastic real estate agent (🏠), analyze this request and generate a detailed response:

        {''.join(existing_properties) if existing_properties else ''}
        
        User Request: {prompt}

        Create a natural, conversational response that includes:
        1. A brief acknowledgment of their specific needs
        2. 2-3 detailed property suggestions with:
           - Property name and type
           - Price range (maintain consistency with any previously discussed properties)
           - Location and neighborhood
           - Key features and amenities
           - Why this property matches their needs
        3. A follow-up question to refine the search
        
        Make the response friendly and engaging, adding occasional light humor.
        Format properties clearly but keep the tone conversational.
        
        Important Notes:
        - If referring to previously discussed properties, maintain consistency with their details
        - For new properties, ensure price ranges are consistent with similar properties
        - Generate realistic but fictional property details
        - Don't reference external websites or listings
        - If the user is asking about a specific property mentioned before, use those exact details"""

        response = self.generate_response(search_prompt)
        properties_response = response.strip()
        
        # Structure the response
        return {
            "message": f"{greeting}\n\n{properties_response}",
            "details": {
                "type": "property_search",
                "greeting_delay": 2,
                "properties": self._extract_properties_from_response(properties_response)
            }
        }
        
    def _extract_properties_from_response(self, response: str) -> list:
        """Extract and structure property information from the LLM response"""
        extraction_prompt = f"""Extract and structure the property information from this response into JSON format.
        Include for each property:
        - name
        - type
        - price
        - location
        - features (as an array)
        - match_reasons (as an array)

        Response text:
        {response}

        Return only the JSON array of properties."""
        
        try:
            structured_response = self.generate_response(extraction_prompt)
            return json.loads(structured_response)
        except:
            # Fallback to simple structure if JSON parsing fails
            return [{
                "response_text": response,
                "parsed": False
            }]
