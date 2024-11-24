from flask import Flask, request, jsonify, render_template
from model import query_model
from flask_cors import CORS
import argparse

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
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run the Flask app")
    parser.add_argument("--port", type=int, default=80, help="Port to run the Flask app on")
    args = parser.parse_args()

    app.run(host="0.0.0.0", port=args.port)
