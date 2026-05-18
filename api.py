# MJ - Biochemistry AI Tool
# Flask API Backend

from flask import Flask, request, jsonify
from flask_cors import CORS
from database import initialize_database, get_database_connection
from config import APP_NAME, APP_VERSION, DEBUG, FEATURES
from utils import log_message, validate_sequence
import json

app = Flask(__name__)
CORS(app)

# Initialize database on startup
initialize_database()

@app.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    return jsonify({
        "app": APP_NAME,
        "version": APP_VERSION,
        "status": "running",
        "features": FEATURES
    })

@app.route('/api/analyze-sequence', methods=['POST'])
def analyze_sequence():
    """Analyze DNA/RNA/Protein sequence"""
    try:
        data = request.get_json()
        sequence = data.get('sequence', '')
        
        if not sequence:
            return jsonify({"error": "No sequence provided"}), 400
        
        seq_type = validate_sequence(sequence)
        seq_length = len(sequence)
        
        result = {
            "sequence_type": seq_type,
            "length": seq_length,
            "sequence": sequence[:100] + "..." if len(sequence) > 100 else sequence
        }
        
        log_message(f"Analyzed sequence: {seq_type}, Length: {seq_length}")
        return jsonify({"status": "success", "data": result})
    
    except Exception as e:
        log_message(f"Error in analyze_sequence: {str(e)}", "ERROR")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "app": APP_NAME,
        "version": APP_VERSION
    })

@app.route('/api/features', methods=['GET'])
def get_features():
    """Get available features"""
    return jsonify({"features": FEATURES})

if __name__ == '__main__':
    log_message(f"Starting {APP_NAME} v{APP_VERSION}")
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)
