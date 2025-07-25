from .base_agent import BaseAgent
import time
import json

class ClosingAgent(BaseAgent):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.name = "Robert"
        self.emoji = "📝"
        
    def get_greeting(self) -> str:
        """Generate a dynamic, personalized greeting"""
        greeting_prompt = """Generate a friendly, reassuring greeting from Robert, the Closing Specialist (use emoji 📝).
        Make it warm and professional, showing expertise in the closing process.
        Include a brief mention of making the closing process smooth and stress-free."""
        
        response = self.generate_response(greeting_prompt)
        return response.strip()
        
    def process(self, prompt: str) -> dict:
        """Process user request and generate closing guidance"""
        # First, send the greeting
        greeting = self.get_greeting()
        time.sleep(2)  # Add a natural pause
        
        # Generate the closing process response
        closing_prompt = f"""As Robert, a knowledgeable Closing Specialist (📝), create a detailed closing guide:

        User Request: {prompt}

        Create a natural, conversational response that includes:
        1. A brief acknowledgment of their current stage
        2. Detailed closing guidance including:
           - Required documentation
           - Timeline with key dates
           - Inspection requirements
           - Closing costs breakdown
           - Final walkthrough details
           - Property handover process
        3. Key tips for a smooth closing
        4. A follow-up question about their specific concerns
        
        Make the response reassuring and friendly, with occasional light humor.
        Format the information clearly but keep it conversational.
        Include realistic but generated process details.
        
        Important: Generate new, unique guidance each time. Don't reference external websites or specific laws."""

        response = self.generate_response(closing_prompt)
        closing_response = response.strip()
        
        # Structure the response
        return {
            "message": f"{greeting}\n\n{closing_response}",
            "details": {
                "type": "closing",
                "greeting_delay": 2,
                "process": self._extract_closing_details_from_response(closing_response)
            }
        }
        
    def _extract_closing_details_from_response(self, response: str) -> dict:
        """Extract and structure closing process details from the LLM response"""
        extraction_prompt = f"""Extract and structure the closing process details from this response into JSON format.
        Include the following sections:
        - documentation (array of required documents)
        - timeline (array of steps with dates and descriptions)
        - inspections (object with required_inspections, scheduling_info)
        - costs (object with closing_costs_breakdown)
        - walkthrough (object with checklist, scheduling_info)
        - handover (object with process_steps, requirements)
        - tips (array of closing tips)

        Response text:
        {response}

        Return only the JSON object with the structured closing details."""
        
        try:
            structured_response = self.generate_response(extraction_prompt)
            return json.loads(structured_response)
        except:
            # Fallback to simple structure if JSON parsing fails
            return {
                "response_text": response,
                "parsed": False
            }
