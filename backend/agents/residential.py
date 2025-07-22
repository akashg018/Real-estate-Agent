from .base_agent import BaseAgent

class ResidentialAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Mike",
            personality="I specialize in analyzing user housing needs and generating property recommendations using AI insights.",
            emoji="🏠",
            role="Residential Property Specialist"
        )

    def get_response(self, user_message):
        # Step 1: Initial Search
        search_prompt = f"""Analyze this property request and generate initial property matches:
\"\"\"
{user_message}
\"\"\"
Return as JSON with:
{{
    "message": "Engaging welcome and initial findings",
    "properties": [
        {{
            "name": "Unique property name",
            "description": "Vivid property description",
            "price": "Formatted price",
            "key_features": ["3-5 standout features"],
            "location": "Specific neighborhood/area"
        }}
    ]
}}"""
        initial_search = self._get_openai_response(search_prompt)

        # Step 2: Property Analysis
        analysis_prompt = f"""Given these properties and request:
Properties: {initial_search.get('properties', [])}
Request: {user_message}

Analyze fit and provide insights as JSON:
{{
    "message": "Analysis overview with emojis",
    "property_insights": [
        {{
            "name": "Property name",
            "strengths": ["2-3 strong points"],
            "concerns": ["1-2 potential issues"],
            "buyer_fit_score": "1-10 score with explanation"
        }}
    ],
    "market_analysis": {{
        "trends": ["2-3 relevant market trends"],
        "opportunities": ["1-2 unique advantages"],
        "risks": ["1-2 factors to consider"]
    }}
}}"""
        analysis = self._get_openai_response(analysis_prompt)

        # Step 3: Final Recommendations
        recommendations_prompt = f"""Based on analysis:
Analysis: {analysis}
Initial Properties: {initial_search.get('properties', [])}

Provide final recommendations as JSON:
{{
    "message": "Final recommendation summary with emojis",
    "top_picks": [
        {{
            "name": "Property name",
            "features": ["Key features"],
            "price": "Formatted price",
            "availability": "Current status",
            "highlight": "Standout selling point",
            "why_recommended": "Personalized explanation"
        }}
    ],
    "next_steps": ["2-3 suggested actions"],
    "timeline": "Estimated viewing/purchase timeline"
}}"""
        recommendations = self._get_openai_response(recommendations_prompt)

        # Combine all insights
        return {
            "initial_search": initial_search,
            "analysis": analysis,
            "final_recommendations": recommendations,
            "context": {
                "user_requirements": user_message,
                "search_criteria": self._extract_search_criteria(user_message)
            }
        }

    def _extract_search_criteria(self, user_message):
        prompt = f"""Extract key search criteria from:
\"\"\"
{user_message}
\"\"\"

Return as JSON:
{{
    "budget_range": "Extracted or inferred budget",
    "location_preferences": ["Areas mentioned or implied"],
    "must_have_features": ["Required features"],
    "nice_to_have_features": ["Desired but not required"],
    "deal_breakers": ["Absolute no-gos"]
}}"""
        return self._get_openai_response(prompt)

