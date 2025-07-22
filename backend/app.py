from flask import Flask, request, jsonify
from flask_cors import CORS
from agents.orchestrator import OrchestratorAgent
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

orchestrator = OrchestratorAgent()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    response = orchestrator.process_request(user_message)
    print("📤 API Response:", response)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
