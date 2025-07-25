from typing import Dict, List
from .base_agent import BaseAgent
from .property_search import PropertySearchAgent
from .amenities import AmenitiesAgent
from .negotiation import NegotiationAgent
from .closing import ClosingAgent
import google.generativeai as genai
import json

class Orchestrator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-lite')
        
        # Initialize all agents with their personalities
        self.agents = {
            'property_search': {
                'agent': PropertySearchAgent(api_key),
                'name': 'Mike',
                'role': 'Property Search Expert',
                'emoji': '🏠',
                'description': 'Specialized in finding perfect properties based on your requirements'
            },
            'amenities': {
                'agent': AmenitiesAgent(api_key),
                'name': 'Emma',
                'role': 'Amenities Research Specialist',
                'emoji': '🌟',
                'description': 'Researches all amenities within 5 miles of properties'
            },
            'negotiation': {
                'agent': NegotiationAgent(api_key),
                'name': 'Jessica',
                'role': 'Master Negotiator',
                'emoji': '💰',
                'description': 'Expert in property price negotiations and deal-making'
            },
            'closing': {
                'agent': ClosingAgent(api_key),
                'name': 'Robert',
                'role': 'Closing Specialist',
                'emoji': '📝',
                'description': 'Handles all aspects of closing and property handover'
            }
        }
        self.conversation_history = []
        
    def welcome_message(self) -> dict:
        """Return a structured welcome message introducing the team"""
        welcome_msg = {
            "conversation": [
                {
                    "name": "Sarah",
                    "role": "Lead Real Estate Advisor",
                    "emoji": "👱‍♀️",
                    "message": "Welcome! I'm Sarah, your personal Real Estate Advisor. I lead a specialized team of expert agents ready to help you find and secure your perfect property.\n\nLet me introduce you to our team:\n\n",
                    "type": "greeting"
                }
            ]
        }
        
        # Add each agent's introduction
        for agent_info in self.agents.values():
            welcome_msg["conversation"].append({
                "name": agent_info['name'],
                "role": agent_info['role'],
                "emoji": agent_info['emoji'],
                "message": f"Hi! I'm {agent_info['name']}, {agent_info['description']}.",
                "type": "introduction"
            })
            
        # Add final prompt
        welcome_msg["conversation"].append({
            "name": "Sarah",
            "role": "Lead Real Estate Advisor",
            "emoji": "👱‍♀️",
            "message": "\nHow can we help you today? Whether you're looking for a property, need information about amenities, want to negotiate a price, or ready to close a deal, our team is here to assist!",
            "type": "prompt"
        })
        
        return welcome_msg
        
    def determine_agent(self, prompt: str) -> str:
        """Determine which agent should handle the user's request"""
        analysis_prompt = f"""As a Real Estate Team Lead, analyze this user request and determine which specialized agent would be most appropriate to handle it. Consider:

Property Search Agent (Mike):
- Initial property searches
- Finding properties matching specific criteria
- Property recommendations

Amenities Agent (Emma):
- Research nearby amenities
- Neighborhood analysis
- Location-based services within 5 miles

Negotiation Agent (Jessica):
- Price negotiations
- Deal structuring
- Offer strategies

Closing Agent (Robert):
- Closing process
- Documentation
- Final handover

User Request: {prompt}

Respond with just one agent type: property_search, amenities, negotiation, or closing"""
        
        response = self.model.generate_content(analysis_prompt)
        return response.text.strip().lower()
        
    def process_request(self, prompt: str) -> dict:
        """Process the user's request and return a structured response"""
        # Keep track of conversation
        self.conversation_history.append({"role": "user", "message": prompt})
        
        # Determine which agent should handle the request
        agent_type = self.determine_agent(prompt)
        
        if agent_type in self.agents:
            # Get agent info
            agent_info = self.agents[agent_type]
            
            # First, have Sarah acknowledge and hand off
            response = {
                "conversation": [
                    {
                        "name": "Sarah",
                        "role": "Lead Real Estate Advisor",
                        "emoji": "👱‍♀️",
                        "message": f"I'll have {agent_info['name']}, our {agent_info['role']}, assist you with this.",
                        "type": "handoff"
                    }
                ]
            }
            
            try:
                # Get relevant context from conversation history
                context = self._build_context_for_agent(agent_type)
                
                # Process request with the appropriate agent
                agent_response = agent_info['agent'].process(prompt, context)
                
                # Structure the raw response if it's a string
                if isinstance(agent_response, str):
                    agent_response = {
                        "message": agent_response,
                        "details": {}
                    }
                
                # Format and update shared context
                formatted_output = self._format_agent_output(agent_type, agent_response["message"])
                self._update_shared_context(agent_type, formatted_output)
                
                # Add agent's response
                response["conversation"].append({
                    "name": agent_info['name'],
                    "role": agent_info['role'],
                    "emoji": agent_info['emoji'],
                    "message": agent_response["message"],
                    "type": "response",
                    "details": formatted_output
                })
                
                # Keep track of conversation with context
                self.conversation_history.append({
                    "role": "agent",
                    "agent": agent_info['name'],
                    "message": agent_response["message"],
                    "context": formatted_output
                })
                
            except Exception as e:
                # Generate a friendly fallback response based on agent type
                fallback_responses = {
                    'property_search': "I understand you're looking for a property. Could you tell me more about what you're looking for in terms of location, budget, and size?",
                    'amenities': "I'd be happy to check the amenities. Could you specify which property or area you're interested in?",
                    'negotiation': "I'll help you negotiate the best price. Could you confirm which property you're interested in?",
                    'closing': "I'll assist with the closing process. Could you specify which property you're planning to move forward with?"
                }
                
                friendly_response = fallback_responses.get(
                    agent_type,
                    f"I'll help you with that! Could you provide a few more details about what you're looking for?"
                )
                
                response["conversation"].append({
                    "name": agent_info['name'],
                    "role": agent_info['role'],
                    "emoji": agent_info['emoji'],
                    "message": friendly_response,
                    "type": "clarification"
                })
            
            return response
            
        else:
            # If we can't determine the appropriate agent
            return {
                "conversation": [
                    {
                        "name": "Sarah",
                        "role": "Lead Real Estate Advisor",
                        "emoji": "👱‍♀️",
                        "message": "I apologize, but I'm not sure which of our specialists would be best suited to help with your request. Could you please provide more specific details about what you're looking for?",
                        "type": "clarification"
                    }
                ]
            }
            
    def _format_agent_output(self, agent_type: str, response: str) -> dict:
        """Format the agent response into structured output based on agent type"""
        if agent_type == "property_search":
            return {
                "final_recommendations": {
                    "properties": [
                        self._extract_property_info(response)
                    ]
                }
            }
        elif agent_type == "amenities":
            return {
                "nearby_amenities": self._extract_amenities_info(response)
            }
        elif agent_type == "negotiation":
            return {
                "strategy": {
                    "message": response,
                    "points": self._extract_negotiation_points(response)
                }
            }
        elif agent_type == "closing":
            return {
                "closing_details": self._extract_closing_info(response)
            }
        return {}
        
    def _extract_property_info(self, response: str) -> dict:
        """Extract property information from the response"""
        lines = response.split('\n')
        property_info = {
            "name": "",
            "price": "",
            "highlight": "",
            "features": []
        }
        
        for line in lines:
            if line.strip():
                if not property_info["name"]:
                    property_info["name"] = line.strip()
                elif "price" in line.lower() and not property_info["price"]:
                    property_info["price"] = line.strip()
                elif not property_info["highlight"]:
                    property_info["highlight"] = line.strip()
                else:
                    property_info["features"].append(line.strip())
                    
        return property_info
        
    def _extract_amenities_info(self, response: str) -> list:
        """Extract amenities information from the response"""
        lines = response.split('\n')
        amenities = []
        current_category = ""
        
        for line in lines:
            if line.strip():
                if line.endswith(':'):
                    current_category = line.strip(':')
                else:
                    amenities.append({
                        "amenity": line.strip(),
                        "category": current_category,
                        "distance": "Nearby",
                        "details": ""
                    })
        
        return amenities
        
    def _extract_negotiation_points(self, response: str) -> list:
        """Extract negotiation points from the response"""
        lines = response.split('\n')
        points = []
        
        for line in lines:
            if line.strip() and not line.endswith(':'):
                points.append(line.strip())
                
        return points
        
    def _extract_closing_info(self, response: str) -> dict:
        """Extract closing information from the response"""
        lines = response.split('\n')
        closing_info = {
            "documents_needed": [],
            "timeline": [],
            "key_terms": {}
        }
        
        current_section = None
        for line in lines:
            if line.strip():
                if "document" in line.lower():
                    current_section = "documents"
                elif "timeline" in line.lower():
                    current_section = "timeline"
                elif ":" in line:
                    key, value = line.split(":", 1)
                    closing_info["key_terms"][key.strip()] = value.strip()
                elif current_section == "documents":
                    closing_info["documents_needed"].append(line.strip())
                elif current_section == "timeline":
                    closing_info["timeline"].append(line.strip())
                    
        return closing_info
        
    def _build_context_for_agent(self, agent_type: str) -> dict:
        """Build relevant context for the agent based on conversation history"""
        context = {
            "properties": [],
            "amenities": [],
            "negotiation": {},
            "closing": {}
        }
        
        # Go through conversation history in reverse to get most recent context
        for entry in reversed(self.conversation_history):
            if entry["role"] == "agent" and "context" in entry:
                if "final_recommendations" in entry["context"]:
                    for prop in entry["context"]["final_recommendations"]["properties"]:
                        if prop not in context["properties"]:
                            context["properties"].append(prop)
                            
                elif "nearby_amenities" in entry["context"]:
                    for amenity in entry["context"]["nearby_amenities"]:
                        if amenity not in context["amenities"]:
                            context["amenities"].append(amenity)
                            
                elif "strategy" in entry["context"]:
                    context["negotiation"].update(entry["context"]["strategy"])
                    
                elif "closing_details" in entry["context"]:
                    context["closing"].update(entry["context"]["closing_details"])
        
        return context
        
    def _update_shared_context(self, agent_type: str, new_context: dict):
        """Update the shared context with new information from an agent"""
        # Update the context of the specific agent
        agent = self.agents[agent_type]["agent"]
        agent.update_shared_context(new_context)
        
        # Share relevant information with other agents
        for other_type, other_info in self.agents.items():
            if other_type != agent_type:
                other_agent = other_info["agent"]
                # Share only relevant information based on agent type
                shared_info = self._filter_context_for_agent(other_type, new_context)
                other_agent.update_shared_context(shared_info)
                
    def _filter_context_for_agent(self, agent_type: str, context: dict) -> dict:
        """Filter context based on what's relevant for each agent type"""
        filtered_context = {}
        
        if agent_type == "property_search":
            # Property search needs to know about prices and features
            if "final_recommendations" in context:
                filtered_context["properties"] = context["final_recommendations"]["properties"]
            if "strategy" in context and "price" in context["strategy"]:
                filtered_context["negotiation"] = {"price": context["strategy"]["price"]}
                
        elif agent_type == "amenities":
            # Amenities agent needs property locations
            if "final_recommendations" in context:
                filtered_context["properties"] = [{
                    "name": p["name"],
                    "location": p.get("location", "Unknown")
                } for p in context["final_recommendations"]["properties"]]
                
        elif agent_type == "negotiation":
            # Negotiation agent needs property details and prices
            if "final_recommendations" in context:
                filtered_context["properties"] = context["final_recommendations"]["properties"]
            if "nearby_amenities" in context:
                filtered_context["amenities"] = context["nearby_amenities"]
                
        elif agent_type == "closing":
            # Closing agent needs all details
            filtered_context = context
            
        return filtered_context
