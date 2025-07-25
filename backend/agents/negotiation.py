from .base_agent import BaseAgent
import time
import json

class NegotiationAgent(BaseAgent):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.name = "Jessica"
        self.emoji = "💰"
        
    def get_greeting(self) -> str:
        """Generate a dynamic, personalized greeting"""
        greeting_prompt = """Generate a friendly, confident greeting from Jessica, the Master Negotiator (use emoji 💰).
        Make it warm and professional, showing expertise in real estate negotiations.
        Include a brief mention of helping them get the best deal possible."""
        
        response = self.generate_response(greeting_prompt)
        return response.strip()
        
    def process(self, prompt: str, context: dict = None) -> dict:
        """Process user request and generate negotiation strategy with context awareness"""
        # First, send the greeting
        greeting = self.get_greeting()
        time.sleep(2)  # Add a natural pause
        
        # Build context-aware prompt
        context_info = ""
        initial_price = None
        property_details = []
        
        if context and "properties" in context:
            for prop in context["properties"]:
                if "price" in prop:
                    initial_price = prop["price"]
                    property_details.append(f"Property: {prop['name']}")
                    property_details.append(f"Listed Price: {prop['price']}")
                    if "features" in prop:
                        property_details.append("Key Features: " + ", ".join(prop["features"]))
                    property_details.append("")
        
        if property_details:
            context_info = "Current Property Details:\n" + "\n".join(property_details)
        
        # Generate the negotiation response
        strategy_prompt = f"""As Jessica, a confident Master Negotiator (💰), create a detailed negotiation strategy:

        {context_info}
        User Request: {prompt}

        Create a natural, conversational response that includes:
        1. A brief analysis of the situation
        2. Detailed negotiation strategy including:
           - Market analysis
           - Property value assessment (must be consistent with the listed price of {initial_price if initial_price else 'the property'})
           - Leverage points
           - Specific offer suggestions
           - Counter-offer scenarios
           - Timeline recommendations
        3. A few key negotiation tips
        4. A follow-up question to refine the strategy
        
        Make the response confident but friendly, with occasional light humor.
        Format the strategy clearly but keep it conversational.
        
        Important Notes:
        - Ensure all price discussions are consistent with the listed price of {initial_price if initial_price else 'the property'}
        - Your negotiation strategy should be realistic based on the actual property details provided
        - Generate market insights that align with the property's features and value
        - Don't reference external market data or websites"""

        response = self.generate_response(strategy_prompt)
        negotiation_response = response.strip()
        
        # Structure the response
        return {
            "message": f"{greeting}\n\n{negotiation_response}",
            "details": {
                "type": "negotiation",
                "greeting_delay": 2,
                "strategy": self._extract_strategy_from_response(negotiation_response)
            }
        }
        
    def _extract_strategy_from_response(self, response: str) -> dict:
        """Extract and structure negotiation strategy from the LLM response"""
        extraction_prompt = f"""Extract and structure the negotiation strategy from this response into JSON format.
        Include the following sections:
        - market_analysis (object with current_conditions, trends)
        - property_valuation (object with suggested_value, value_factors)
        - negotiation_points (array of key points)
        - offer_strategy (object with initial_offer, counter_scenarios)
        - timeline (array of steps with descriptions)
        - tips (array of negotiation tips)

        Response text:
        {response}

        Return only the JSON object with the structured strategy."""
        
        try:
            structured_response = self.generate_response(extraction_prompt)
            return json.loads(structured_response)
        except:
            # Fallback to simple structure if JSON parsing fails
            return {
                "response_text": response,
                "parsed": False
            }
