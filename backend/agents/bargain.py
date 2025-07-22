from .base_agent import BaseAgent

class BargainAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Jessica",
            personality="I'm a sharp-witted negotiator with a talent for finding the sweet spot in every deal. I love using charm and data to get the best prices, and I always keep things light with my negotiation puns!",
            emoji="💰",
            role="Master Negotiator"
        )

    def get_response(self, property_info):
        # Step 1: Market Analysis
        market_prompt = f"""Analyze market position for properties:
{property_info.get('initial_search', {}).get('properties', [])}

Search context:
{property_info.get('context', {})}

Return detailed market analysis as JSON:
{{
    "message": "Market overview with negotiation joke",
    "market_conditions": {{
        "overall_trend": "Market direction with emojis",
        "price_analysis": ["3-4 price insights"],
        "competition_level": "Buyer/Seller market status",
        "time_on_market": "Average days properties are listed",
        "seasonal_factors": ["1-2 seasonal impacts"]
    }},
    "property_positions": [
        {{
            "name": "Property name",
            "list_price": "Current price",
            "fair_value": "Estimated fair market value",
            "negotiation_margin": "Estimated room for negotiation",
            "justification": ["2-3 value factors"]
        }}
    ]
}}"""
        market_analysis = self._get_openai_response(market_prompt)

        # Step 2: Negotiation Strategy
        strategy_prompt = f"""Based on market analysis:
{market_analysis}

Develop negotiation strategies for each property as JSON:
{{
    "message": "Strategy overview with emojis",
    "property_strategies": [
        {{
            "property": "Property name",
            "initial_offer": {{
                "amount": "Suggested first offer",
                "reasoning": "Why this amount",
                "timing": "When to make offer"
            }},
            "negotiation_points": [
                {{
                    "point": "Specific negotiation point",
                    "leverage": "How to use this advantage",
                    "fallback": "Alternative position"
                }}
            ],
            "deal_sweeteners": ["2-3 non-price negotiation items"]
        }}
    ],
    "general_tactics": ["3-4 overall negotiation approaches"]
}}"""
        negotiation_strategy = self._get_openai_response(strategy_prompt)

        # Step 3: Risk Assessment and Timeline
        timeline_prompt = f"""For these properties and strategies:
{negotiation_strategy}

Provide negotiation timeline and risk assessment as JSON:
{{
    "message": "Timeline overview with emojis",
    "risk_assessment": {{
        "market_risks": ["2-3 market-related risks"],
        "property_risks": ["2-3 property-specific risks"],
        "mitigation_strategies": ["2-3 risk management approaches"]
    }},
    "expected_outcomes": [
        {{
            "property": "Property name",
            "best_case": "Best possible price",
            "realistic": "Most likely outcome",
            "walkaway": "Minimum acceptable terms"
        }}
    ],
    "timeline": {{
        "preparation": ["2-3 preparation steps"],
        "negotiation": ["3-4 negotiation phases"],
        "closing": ["2-3 closing steps"]
    }}
}}"""
        timeline_and_risks = self._get_openai_response(timeline_prompt)

        return {
            "introduction": {
                "message": market_analysis.get("message", "Let's negotiate! 💰"),
                "market_overview": market_analysis.get("market_conditions", {})
            },
            "analysis": market_analysis,
            "strategy": negotiation_strategy,
            "timeline_and_risks": timeline_and_risks,
            "negotiation_points": [
                point for strategy in negotiation_strategy.get("property_strategies", [])
                for point in strategy.get("negotiation_points", [])
            ]
        }
