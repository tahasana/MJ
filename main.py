import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from database import initialize_database, get_database_connection

# Initialize the Flask application instance
app = Flask(__name__)

# Enable CORS so your GitHub Pages frontend can access this backend securely
CORS(app)

# Initialize your database connection safely when the app boots up
try:
    initialize_database()
except Exception as e:
    print(f"Database initialization warning/error: {e}")

# Define your MJBiochemist class with standard initialization so it doesn't cause syntax errors
class MJBiochemist:
    def __init__(self):
        pass

    def analyze_data(self, data):
        # Placeholder for your biochemistry analysis logic
        return {"status": "success", "message": "Data analyzed successfully"}

# Base health-check route to confirm the server is live
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "online",
        "message": "MJ Biochemistry AI Tool Backend is running perfectly!"
    }), 200

# Sample API route for your biochemistry analysis
@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Using the class instance safely
        biochemist = MJBiochemist()
        result = biochemist.analyze_data(data)
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# This block ensures it runs perfectly if you ever want to test it locally too
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
