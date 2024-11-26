from flask import Flask, request, jsonify, render_template
from langchain_ollama import OllamaLLM

from model import query_model
from flask_cors import CORS
import argparse
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def handle_query():
    data = request.json
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        answer = query_model(question)
        return jsonify({"answer": answer})
    except Exception as e:
        logger.info(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/test_ollama', methods=['GET'])
def test_ollama():
    try:
        llm = OllamaLLM(
            model="phi3:mini",
            base_url="http://127.0.0.1:11434"
        )
        response = llm("What are Arvin's main skills?")
        return jsonify({"response": response})
    except Exception as e:
        app.logger.error(f"Error connecting to Ollama: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run the Flask app")
    parser.add_argument("--port", type=int, default=80, help="Port to run the Flask app on")
    args = parser.parse_args()

    app.run(host="0.0.0.0", port=args.port)
