import os
import google.generativeai as genai
from utils.json_helper import ensure_json_response

class BaseAgent:
    def __init__(self, name, personality, emoji, role):
        self.name = name
        self.personality = personality
        self.emoji = emoji
        self.role = role
        self.api_key = os.getenv('GEMINI_API_KEY')
        print(f"🔑 Using Gemini API Key: {self.api_key[:5]}..." if self.api_key else "⚠️ GEMINI_API_KEY not found!")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash-latest')

        self.generation_config = {
            'temperature': 0.9,
            'top_p': 0.9,
            'top_k': 40,
            'max_output_tokens': 2048,
        }

    def get_greeting(self):
        prompt = f"""
As {self.name}, generate a friendly greeting and introduction.
You are a {self.role} with this personality: {self.personality}
Include a humorous comment or joke related to real estate.

Format response as JSON:
{{
    "greeting": "Your greeting with emojis",
    "introduction": "Brief role description",
    "joke": "Your real estate related joke"
}}
"""
        return self._get_openai_response(prompt)

    def get_handoff_message(self, next_agent_name=None):
        if next_agent_name:
            prompt = f"""
Generate a friendly handoff message from {self.name} to {next_agent_name}.
Include a brief summary of what you've done and why you're handing off.

Format as JSON:
{{
    "message": "Your handoff message with emojis",
    "summary": "Brief summary of your work"
}}
"""
        else:
            prompt = f"""
Generate a friendly closing message from {self.name}.
Include a positive note about the assistance provided.

Format as JSON:
{{
    "message": "Your closing message with emojis",
    "summary": "Brief summary of help provided"
}}
"""
        return self._get_openai_response(prompt)

    def _get_openai_response(self, prompt, context=None):
        try:
            context_text = ""
            if context:
                context_text = f"\n\nAdditional context:\n{context}"

            full_prompt = f"""You are {self.name}, a {self.role}. {self.personality}
Your signature emoji is {self.emoji}.

IMPORTANT: Your response must be valid JSON only. Do not include any other text.
Always include emojis in your responses to make them friendly and engaging.

{prompt}{context_text}
"""

            response = self.model.generate_content(
                full_prompt,
                generation_config=self.generation_config
            )

            result = ensure_json_response(response.text)
            print(f"{self.emoji} {self.name} Response:", result)
            return result

        except Exception as e:
            print(f"❌ {self.name} Error: {e}")
            return {
                "error": str(e),
                "message": f"Oops! {self.emoji} Having some technical difficulties. Let me get that fixed for you!"
            }
