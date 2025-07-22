from .base_agent import BaseAgent

class ContractAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Robert",
            personality="I'm Robert, your friendly legal eagle! 📝 I'll simplify contracts and throw in a lawyer joke or two!",
            emoji="📝",
            role="Legal Expert"
        )

    def get_response(self, deal_info):
        negotiation_points = deal_info.get('negotiation_points', [])

        context = {
            "role": "Legal Expert",
            "personality": self.personality,
            "negotiation_points": negotiation_points
        }

        contract_details = {
            "initial_search": {
                "message": self._get_openai_response(
                    "As a legal expert, provide an initial message about reviewing the properties.",
                    context
                ),
                "contracts": []
            },
            "analysis": {
                "message": "📋 Here are the key legal points to consider:",
                "points": self._format_list_response(
                    self._get_openai_response(
                        "Provide a list of key legal points to consider for these properties.",
                        context
                    )
                )
            },
            "final_recommendations": {
                "message": "⚖️ Here's my legal assessment and recommendations:",
                "documents_needed": self._format_list_response(
                    self._get_openai_response(
                        "List the essential documents needed for the rental application process.",
                        context
                    )
                ),
                "legal_timeline": self._format_list_response(
                    self._get_openai_response(
                        "Provide a timeline of the legal process for these properties.",
                        context
                    )
                )
            }
        }

        for deal in negotiation_points:
            property_name = deal.get('property', '')
            price = deal.get('suggested_offer', '$0')

            property_context = {
                **context,
                "property_name": property_name,
                "price": price
            }

            key_terms_response = self._get_openai_response(
                f"Provide key legal terms for the property '{property_name}' with price {price}. "
                "Include deposit, lease term, inspection period, notice period, pet policy, and utilities information.",
                property_context
            )

            key_terms = self._parse_key_terms(key_terms_response)

            contract_details['initial_search']['contracts'].append({
                "property": property_name,
                "key_terms": key_terms
            })

        return contract_details

    def _format_list_response(self, response):
        if isinstance(response, str):
            return response.split('\n')
        return response

    def _parse_key_terms(self, response):
        if isinstance(response, dict):
            return response

        terms_dict = {}
        if isinstance(response, str):
            for line in response.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    terms_dict[key.strip().lower().replace(' ', '_')] = value.strip()
        return terms_dict
