import json
import re

def ensure_json_response(response_text):
    """
    Cleans markdown-style blocks, extracts JSON, and ensures valid JSON response.
    Handles both parsed dicts and JSON strings.
    """
    if isinstance(response_text, (dict, list)):
        return response_text

    if not response_text:
        return {"error": "Empty response"}

    try:
        # Step 1: Remove markdown code block markers if present
        cleaned_text = re.sub(r"```json|```", "", str(response_text)).strip()

        # Step 2: Try to parse full cleaned response
        return json.loads(cleaned_text)

    except (json.JSONDecodeError, TypeError):
        # Step 3: Fallback - extract substring between first '{' and last '}'
        try:
            start = cleaned_text.find('{')
            end = cleaned_text.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = cleaned_text[start:end]
                return json.loads(json_str)
        except Exception:
            pass

    # Step 4: Total failure - return as plain text with error
    return {
        "text": str(response_text),
        "error": "Response was not in JSON format"
    }
