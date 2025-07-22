from .base_agent import BaseAgent

class LifestyleAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Emma",
            personality="I'm Emma, your neighborhood insider! 🌟 Let me show you around with local secrets and foodie tips!",
            emoji="🌟",
            role="Neighborhood Expert"
        )


    def get_response(self, property_info):
        # Step 1: Lifestyle Profile Analysis
        profile_prompt = f"""Based on user requirements:
{property_info.get('context', {}).get('user_requirements', '')}

Create lifestyle profile as JSON:
{{
    "message": "Lifestyle overview with emojis",
    "lifestyle_preferences": {{
        "activity_level": "Active/Moderate/Relaxed",
        "social_style": "Social butterfly/Balanced/Private",
        "daily_routine": ["3-4 typical daily activities"],
        "weekend_interests": ["2-3 weekend activities"],
        "important_factors": ["3-4 lifestyle priorities"]
    }},
    "community_needs": ["4-5 community features needed"]
}}"""
        lifestyle_profile = self._get_openai_response(profile_prompt)

        # Step 2: Property Lifestyle Match
        properties = property_info.get('initial_search', {}).get('properties', [])
        match_prompt = f"""Analyze lifestyle fit for properties:
{properties}

Based on profile:
{lifestyle_profile}

Return as JSON:
{{
    "message": "Lifestyle match overview with emojis",
    "property_matches": [
        {{
            "property": "Property name",
            "lifestyle_score": "1-10 with explanation",
            "perfect_for": ["2-3 ideal lifestyle aspects"],
            "challenges": ["1-2 lifestyle challenges"],
            "nearby_amenities": {{
                "dining": ["2-3 restaurant types/names"],
                "fitness": ["2-3 fitness options"],
                "shopping": ["2-3 shopping venues"],
                "entertainment": ["2-3 entertainment options"],
                "outdoors": ["2-3 outdoor spaces"]
            }},
            "community_vibe": "Neighborhood atmosphere description"
        }}
    ]
}}"""
        property_matches = self._get_openai_response(match_prompt)

        # Step 3: Recommendations and Tips
        recommendations_prompt = f"""Based on lifestyle matches:
{property_matches}

Provide lifestyle recommendations as JSON:
{{
    "message": "Recommendations overview with emojis",
    "top_lifestyle_picks": [
        {{
            "property": "Property name",
            "why_perfect": "Lifestyle fit explanation",
            "local_gems": ["3-4 hidden neighborhood treasures"],
            "lifestyle_tips": ["2-3 tips to maximize location"],
            "community_integration": ["2-3 ways to connect with neighbors"]
        }}
    ],
    "seasonal_activities": {{
        "spring": ["2-3 activities"],
        "summer": ["2-3 activities"],
        "fall": ["2-3 activities"],
        "winter": ["2-3 activities"]
    }},
    "quality_of_life": {{
        "work_life_balance": "How location supports balance",
        "social_opportunities": "Community engagement options",
        "wellness_factors": ["2-3 health/wellness benefits"]
    }}
}}"""
        lifestyle_recommendations = self._get_openai_response(recommendations_prompt)

        return {
            "lifestyle_profile": lifestyle_profile,
            "property_matches": property_matches,
            "recommendations": lifestyle_recommendations,
            "highlighted_amenities": {
                prop["property"]: prop.get("nearby_amenities", {})
                for prop in property_matches.get("property_matches", [])
            }
        }
