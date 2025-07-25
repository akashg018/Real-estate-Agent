from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.orchestrator import Orchestrator
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"], "methods": ["GET", "POST", "OPTIONS"]}})

# Get API key from environment
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Initialize orchestrator
orchestrator = Orchestrator(api_key)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/welcome', methods=['GET'])
def get_welcome():
    try:
        response = orchestrator.welcome_message()
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error getting welcome message: {str(e)}")
        return jsonify({"error": "Failed to get welcome message"}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        if not data or 'message' not in data:
            return jsonify({"error": "No message provided"}), 400
        
        message = data['message']
        response = orchestrator.process_request(message)
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        return jsonify({"error": "Failed to process your request"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
