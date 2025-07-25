import google.generativeai as genai
from abc import ABC, abstractmethod
import logging
import json
from utils.logger import setup_logger

class BaseAgent(ABC):
    def __init__(self, api_key):
        self.logger = setup_logger()
        self.logger.info(f"Initializing {self.__class__.__name__}")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-lite')
        self.shared_context = {}
        
    @abstractmethod
    def process(self, prompt: str, context: dict = None) -> dict:
        """
        Process a user prompt and return a structured response
        
        Args:
            prompt (str): The user's input prompt
            context (dict): Optional context from previous interactions
            
        Returns:
            dict: A structured response with agent details and message
        """
        pass
    
    def generate_response(self, prompt: str, context: dict = None) -> dict:
        """Generate a response using the Gemini model with context awareness"""
        self.logger.info(f"{self.__class__.__name__} generating response")
        
        # Add context to the prompt if available
        if context:
            context_str = self._format_context_for_prompt(context)
            enhanced_prompt = f"""Previous Context:
{context_str}

Current Request:
{prompt}

Important: Ensure your response maintains consistency with the previous context, especially regarding:
- Property prices and details
- Location information
- Amenities mentioned
- Any negotiation points or terms discussed

Your response:"""
        else:
            enhanced_prompt = prompt
            
        try:
            response = self.model.generate_content(enhanced_prompt)
            self.logger.info(f"{self.__class__.__name__} response generated successfully")
            
            # Try to parse the response as JSON if it's in JSON format
            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                # If not JSON, return as regular text
                return response.text
                
        except Exception as e:
            self.logger.error(f"{self.__class__.__name__} error generating response: {str(e)}")
            raise
            
    def _format_context_for_prompt(self, context: dict) -> str:
        """Format the context into a string for the prompt"""
        context_str = []
        
        if 'properties' in context:
            for prop in context['properties']:
                context_str.append(f"Property: {prop['name']}")
                context_str.append(f"Price: {prop['price']}")
                context_str.append(f"Location: {prop.get('location', 'Not specified')}")
                if 'features' in prop:
                    context_str.append("Features: " + ", ".join(prop['features']))
                context_str.append("")
                
        if 'amenities' in context:
            context_str.append("Nearby Amenities:")
            for amenity in context['amenities']:
                context_str.append(f"- {amenity['name']} ({amenity.get('distance', 'nearby')})")
            context_str.append("")
                
        if 'negotiation' in context:
            context_str.append("Negotiation Details:")
            context_str.append(f"Initial Price: {context['negotiation'].get('initial_price', 'Not specified')}")
            context_str.append(f"Current Stage: {context['negotiation'].get('stage', 'Not specified')}")
            context_str.append("")
            
        return "\n".join(context_str)
            
    def _format_response(self, message: str, details: dict = None) -> dict:
        """Format the agent's response into a structured format"""
        return {
            "message": message,
            "details": details if details else {}
        }
        
    def update_shared_context(self, context: dict):
        """Update the shared context with new information"""
        self.shared_context.update(context)
        
    def get_shared_context(self) -> dict:
        """Get the current shared context"""
        return self.shared_context.copy()
