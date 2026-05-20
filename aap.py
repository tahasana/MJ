import os
import math
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class MJBiochemist:
    def __init__(self):
        self.codon_table = {
            'AUA':'I', 'AUC':'I', 'AUU':'I', 'AUG':'M', 'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACU':'T',
            'AAC':'N', 'AAU':'N', 'AAA':'K', 'AAG':'K', 'AGC':'S', 'AGU':'S', 'AGA':'R', 'AGG':'R',
            'CUA':'L', 'CUC':'L', 'CUU':'L', 'CUG':'L', 'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCU':'P',
            'CAC':'H', 'CAU':'H', 'CAA':'Q', 'CAG':'Q', 'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGU':'R',
            'GUA':'V', 'GUC':'V', 'GUU':'V', 'GUG':'V', 'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCU':'A',
            'GAC':'D', 'GAU':'D', 'GAA':'E', 'GAG':'E', 'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGU':'G',
            'UCA':'S', 'UCC':'S', 'UCG':'S', 'UCU':'S', 'UAC':'Y', 'UAU':'Y', 'UAA':'_Stop_', 'UAG':'_Stop_',
            'UGC':'C', 'UGU':'C', 'UGA':'_Stop_', 'UGG':'W',
        }
        self.mw_table = {
            'A': 71.08, 'R': 156.19, 'N': 114.10, 'D': 115.09, 'C': 103.14, 'E': 129.12, 
            'Q': 128.13, 'G': 57.05, 'H': 137.14, 'I': 113.16, 'L': 113.16, 'K': 128.17, 
            'M': 131.20, 'F': 147.18, 'P': 97.12, 'S': 87.08, 'T': 101.11, 'W': 186.21, 
            'Y': 163.18, 'V': 99.13
        }

    def analyze_sequence(self, raw_sequence):
        seq = raw_sequence.upper().strip().replace(" ", "").replace("\n", "").replace("\r", "")
        length = len(seq)
        if length == 0:
            return {"success": False, "error": "Empty sequence string provided."}

        has_t, has_u = 'T' in seq, 'U' in seq
        nucleic_bases = set(['A', 'T', 'C', 'G', 'U', 'N'])
        is_nucleic = set(seq).issubset(nucleic_bases) or (len(set(seq) - nucleic_bases) / len(seq) < 0.2)

        if has_t and has_u: seq_type = "Mutated/Mixed Nucleic Acid"
        elif has_u and is_nucleic: seq_type = "RNA"
        elif is_nucleic: seq_type = "DNA"
        else: seq_type = "Protein Peptide Chain"

        counts = {b: seq.count(b) for b in ['A', 'T', 'C', 'G', 'U']}
        g_c_sum = counts['G'] + counts['C']
        total_bases = sum(counts.values())
        gc_content = round((g_c_sum / total_bases) * 100, 2) if total_bases > 0 else 0

        protein_translation = ""
        mol_weight = 0
        
        if seq_type in ["DNA", "RNA"]:
            rna_seq = seq if seq_type == "RNA" else seq.replace('T', 'U')
            proteins = []
            for i in range(0, len(rna_seq) - 2, 3):
                amino_acid = self.codon_table.get(rna_seq[i:i+3], "?")
                if amino_acid == "_Stop_": break
                if amino_acid != "?": proteins.append(amino_acid)
            protein_translation = "".join(proteins)
            mol_weight = sum(self.mw_table.get(aa, 0) for aa in protein_translation) + 18.02 if protein_translation else 0
        else:
            protein_translation = seq
            mol_weight = sum(self.mw_table.get(aa, 0) for aa in seq) + 18.02 if seq else 0

        return {
            "success": True,
            "analysis": {
                "sequence_type": seq_type,
                "length": length,
                "gc_content": gc_content if seq_type in ["DNA", "RNA"] else "N/A",
                "protein_translation": protein_translation,
                "molecular_weight": round(mol_weight, 2)
            }
        }

    def process_experimental_data(self, raw_data_string):
        try:
            cleaned = raw_data_string.replace('\n', ',').replace(' ', ',').replace('\r', ',')
            parts = [p.strip() for p in cleaned.split(',') if p.strip()]
            numbers = [float(n) for n in parts]
            
            if not numbers:
                return {"success": False, "error": "No valid numeric coordinates detected."}
            
            n_count = len(numbers)
            n_mean = sum(numbers) / n_count
            variance = sum((x - n_mean) ** 2 for x in numbers) / n_count
            std_dev = math.sqrt(variance)
            
            anomalies = []
            if std_dev > 0:
                for x in numbers:
                    if abs(x - n_mean) > (3 * std_dev):
                        anomalies.append(x)
            
            return {
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
            }
        except ValueError:
            return {"success": False, "error": "Data matrix contains non-numeric inputs."}

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "online"}), 200

@app.route('/api/analyze-sequence', methods=['POST'])
def analyze_sequence_route():
    try:
        data = request.get_json() or {}
        result = MJBiochemist().analyze_sequence(data.get('sequence', ''))
        return jsonify(result), 200 if result["success"] else 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/analyze-data', methods=['POST'])
def analyze_data_route():
    try:
        data = request.get_json() or {}
        result = MJBiochemist().process_experimental_data(data.get('experimental_data', ''))
        return jsonify(result), 200 if result["success"] else 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
