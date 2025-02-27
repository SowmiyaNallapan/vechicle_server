from flask import Flask, request, jsonify
from flask_cors import CORS  # Ensure CORS is enabled
  # Allow frontend to access API


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json  # Get JSON data from frontend
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing fields"}), 400

    return jsonify({"message": "User registered successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)
