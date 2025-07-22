from .base_agent import BaseAgent
from .bargain import BargainAgent
from .contract import ContractAgent
from .lifestyle import LifestyleAgent
from .location import LocationAgent
from .residential import ResidentialAgent

class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Sarah",
            personality="I'm Sarah, your real estate team leader! 🎭 I'll coordinate everything to make your property search smooth and clear.",
            emoji="🎭",
            role="Real Estate Team Lead"
        )
        self.residential_agent = ResidentialAgent()
        self.bargain_agent = BargainAgent()
        self.contract_agent = ContractAgent()
        self.lifestyle_agent = LifestyleAgent()
        self.location_agent = LocationAgent()

    def process_request(self, user_message):
        conversation_steps = []
        context = {"user_message": user_message}

        # Step 1: Mike (ResidentialAgent)
        residential_data = self.residential_agent.get_response(user_message)
        context["residential"] = residential_data
        
        conversation_steps.extend([
            {
                "name": "Mike",
                "role": "Residential Property Specialist",
                "emoji": "🏠",
                "type": "property_search",
                "message": residential_data.get('initial_search', {}).get('message', ""),
                "output": residential_data,
                "timestamp": self._get_timestamp()
            },
            self._get_handoff_message("Mike", "Jessica", residential_data)
        ])

        # Step 2: Jessica (BargainAgent)
        bargain_data = self.bargain_agent.get_response(residential_data)
        context["bargain"] = bargain_data
        
        conversation_steps.extend([
            {
                "name": "Jessica",
                "role": "Negotiation Specialist",
                "emoji": "💰",
                "type": "negotiation",
                "message": bargain_data.get('introduction', {}).get('message', ""),
                "output": bargain_data,
                "timestamp": self._get_timestamp()
            },
            self._get_handoff_message("Jessica", "Robert", bargain_data)
        ])

        # Step 3: Robert (ContractAgent)
        contract_context = {
            **context,
            "negotiation_points": bargain_data.get("negotiation_points", [])
        }
        contract_data = self.contract_agent.get_response(contract_context)
        context["contract"] = contract_data
        
        conversation_steps.extend([
            {
                "name": "Robert",
                "role": "Legal Advisor",
                "emoji": "⚖️",
                "type": "legal",
                "message": contract_data.get('initial_search', {}).get('message', ""),
                "output": contract_data,
                "timestamp": self._get_timestamp()
            },
            self._get_handoff_message("Robert", "Emma", contract_data)
        ])

        # Step 4: Emma (LifestyleAgent)
        lifestyle_context = {
            **context,
            "properties": residential_data.get('initial_search', {}).get('properties', [])
        }
        lifestyle_data = self.lifestyle_agent.get_response(lifestyle_context)
        context["lifestyle"] = lifestyle_data
        
        conversation_steps.extend([
            {
                "name": "Emma",
                "role": "Lifestyle Consultant",
                "emoji": "🌟",
                "type": "lifestyle",
                "message": lifestyle_data.get('lifestyle_profile', {}).get('message', ""),
                "output": lifestyle_data,
                "timestamp": self._get_timestamp()
            },
            self._get_handoff_message("Emma", "Jack", lifestyle_data)
        ])

        # Step 5: Jack (LocationAgent)
        location_context = {
            **context,
            "lifestyle_preferences": lifestyle_data.get('lifestyle_profile', {}).get('lifestyle_preferences', {})
        }
        location_data = self.location_agent.get_response(location_context)
        context["location"] = location_data
        
        conversation_steps.extend([
            {
                "name": "Jack",
                "role": "Location Expert",
                "emoji": "🗺️",
                "type": "location",
                "message": location_data.get('overview', {}).get('message', ""),
                "output": location_data,
                "timestamp": self._get_timestamp()
            },
            self._get_handoff_message("Jack", None, location_data)
        ])

        # Final Summary from Sarah
        summary_prompt = f"""Based on all agent inputs:
User Request: {user_message}

Mike's Properties: {residential_data.get('final_recommendations', {})}
Jessica's Negotiation: {bargain_data.get('strategy', {})}
Robert's Legal: {contract_data.get('final_recommendations', {})}
Emma's Lifestyle: {lifestyle_data.get('recommendations', {})}
Jack's Location: {location_data.get('recommendations', {})}

Provide a final recommendation as JSON:
{{
    "message": "Final summary with emojis",
    "top_properties": [
        {{
            "name": "Property name",
            "overall_score": "1-10 with explanation",
            "key_advantages": ["3-4 main selling points"],
            "considerations": ["1-2 things to keep in mind"],
            "next_steps": ["2-3 immediate actions"]
        }}
    ],
    "team_insights": {{
        "residential": "Key property insights",
        "negotiation": "Main negotiation opportunities",
        "legal": "Important legal considerations",
        "lifestyle": "Lifestyle alignment highlights",
        "location": "Location advantages"
    }},
    "action_plan": ["3-4 recommended next steps"],
    "timeline": "Estimated timeline for viewing/offer/closing"
}}"""
        
        final_summary = self._get_openai_response(summary_prompt)
        
        conversation_steps.append({
            "name": "Sarah",
            "role": "Real Estate Team Lead",
            "emoji": "🎭",
            "type": "summary",
            "message": final_summary.get('message', ""),
            "output": {
                "summary": final_summary,
                "context": context
            },
            "timestamp": self._get_timestamp()
        })

        return {"conversation": conversation_steps}

    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().isoformat()

    def _get_handoff_message(self, from_agent, to_agent, context):
        if to_agent:
            message_prompt = f"""Create a handoff message from {from_agent} to {to_agent} based on:
{context}

Return as JSON:
{{
    "message": "Friendly handoff with emojis explaining what was done and what's next",
    "key_points": ["2-3 main points to highlight"]
}}"""
        else:
            message_prompt = f"""Create a completion message from {from_agent} based on:
{context}

Return as JSON:
{{
    "message": "Friendly completion message with emojis",
    "key_findings": ["2-3 main findings"]
}}"""

        handoff = self._get_openai_response(message_prompt)
        
        return {
            "name": "Sarah",
            "role": "Real Estate Team Lead",
            "emoji": "🎭",
            "type": "orchestration",
            "message": handoff.get('message', ""),
            "key_points": handoff.get('key_points', handoff.get('key_findings', [])),
            "timestamp": self._get_timestamp()
        }

        conversation_steps.append({
            "name": "Sarah",
            "role": "Real Estate Team Lead",
            "emoji": "🎭",
            "type": "summary",
            "message": final_summary.get('message', "Here's my final recommendation."),
            "output": {
                "residential_summary": residential_data,
                "negotiation_summary": bargain_data,
                "legal_summary": contract_data,
                "lifestyle_summary": lifestyle_data,
                "location_summary": location_data
            }
        })

        return {"conversation": conversation_steps}
