import os
import math
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "online", "message": "MJ System Core Gateway Active"}), 200

@app.route('/api/analyze-sequence', methods=['POST'])
def analyze_sequence():
    try:
        data = request.get_json() or {}
        seq = data.get('sequence', '').upper().strip()
        if not seq:
            return jsonify({"success": False, "error": "No sequence matrix found"}), 400
        
        has_t, has_u = 'T' in seq, 'U' in seq
        if has_t and has_u: seq_type = "Mixed/Mutated Nucleic Acid"
        elif has_u: seq_type = "RNA"
        elif any(b in seq for b in ['A','T','C','G']): seq_type = "DNA"
        else: seq_type = "Protein Peptide Chain"

        return jsonify({
            "success": True,
            "analysis": {
                "sequence_type": seq_type,
                "length": len(seq),
                "gc_content": round(((seq.count('G') + seq.count('C')) / len(seq)) * 100, 2) if len(seq) > 0 else 0
            }
        }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/analyze-data', methods=['POST'])
def analyze_data():
    try:
        data = request.get_json() or {}
        raw_data = data.get('experimental_data', '')
        
        # Clean up string into float arrays
        cleaned = raw_data.replace('\n', ',').replace(' ', ',').replace('\r', ',')
        parts = [p.strip() for p in cleaned.split(',') if p.strip()]
        numbers = [float(n) for n in parts]
        
        if not numbers:
            return jsonify({"success": False, "error": "No valid data detected."}), 400
        
        n_count = len(numbers)
        n_mean = sum(numbers) / n_count
        variance = sum((x - n_mean) ** 2 for x in numbers) / n_count
        std_dev = math.sqrt(variance)
        
        anomalies = []
        if std_dev > 0:
            for x in numbers:
                # Calculate deviations against standard 3-Sigma parameters
                if abs(x - n_mean) > (3 * std_dev):
                    anomalies.append(x)
        
        return jsonify({
            "success": True,
            "results": {
                "count": n_count,
                "mean": round(n_mean, 4),
                "variance": round(variance, 4),
                "std_dev": round(std_dev, 4),
                "max": max(numbers),
                "min": min(numbers),
                "anomalies": anomalies
            }
        }), 200
    except ValueError:
        return jsonify({"success": False, "error": "Input string contains non-numeric characters."}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
