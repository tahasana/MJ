import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class MJBiochemist:
    def __init__(self):
        # Standard Genetic Code Dictionary for translating RNA codons to Amino Acids
        self.codon_table = {
            'AUA':'I', 'AUC':'I', 'AUU':'I', 'AUG':'M',
            'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACU':'T',
            'AAC':'N', 'AAU':'N', 'AAA':'K', 'AAG':'K',
            'AGC':'S', 'AGU':'S', 'AGA':'R', 'AGG':'R',
            'CUA':'L', 'CUC':'L', 'CUU':'L', 'CUG':'L',
            'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCU':'P',
            'CAC':'H', 'CAU':'H', 'CAA':'Q', 'CAG':'Q',
            'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGU':'R',
            'GUA':'V', 'GUC':'V', 'GUU':'V', 'GUG':'V',
            'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCU':'A',
            'GAC':'D', 'GAU':'D', 'GAA':'E', 'GAG':'E',
            'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGU':'G',
            'UCA':'S', 'UCC':'S', 'UCG':'S', 'UCU':'S',
            'UAC':'Y', 'UAU':'Y', 'UAA':'_Stop_', 'UAG':'_Stop_',
            'UGC':'C', 'UGU':'C', 'UGA':'_Stop_', 'UGG':'W',
        }

    def analyze_sequence(self, raw_sequence):
        seq = raw_sequence.upper().strip().replace(" ", "")
        length = len(seq)
        
        if length == 0:
            return {"success": False, "error": "Empty sequence provided."}

        has_t = 'T' in seq
        has_u = 'U' in seq
        
        nucleic_bases = set(['A', 'T', 'C', 'G', 'U', 'N'])
        unique_chars = set(seq)
        is_nucleic = unique_chars.issubset(nucleic_bases) or (len(unique_chars - nucleic_bases) / len(unique_chars) < 0.2)

        if has_t and has_u:
            seq_type = "Mutated/Mixed Nucleic Acid (Contains both T and U)"
        elif has_u and is_nucleic:
            seq_type = "RNA"
        elif is_nucleic:
            seq_type = "DNA"
        else:
            seq_type = "Protein Peptide Chain"

        counts = {
            'A': seq.count('A'),
            'T': seq.count('T'),
            'C': seq.count('C'),
            'G': seq.count('G'),
            'U': seq.count('U')
        }

        g_c_sum = counts['G'] + counts['C']
        total_bases = sum(1 for char in seq if char in ['A', 'T', 'C', 'G', 'U'])
        gc_content = round((g_c_sum / total_bases) * 100, 2) if total_bases > 0 else 0

        transcription = ""
        protein_translation = ""
        
        if seq_type in ["DNA", "RNA"]:
            rna_seq = seq if seq_type == "RNA" else seq.replace('T', 'U')
            transcription = rna_seq
            
            proteins = []
            for i in range(0, len(rna_seq) - 2, 3):
                codon = rna_seq[i:i+3]
                amino_acid = self.codon_table.get(codon, "?")
                if amino_acid == "_Stop_":
                    proteins.append("[STOP]")
                    break
                proteins.append(amino_acid)
            protein_translation = "".join(proteins)

        summary = f"### Structural Breakdown\n"
        summary += f"* **Classification:** Confirmed {seq_type} molecular sequence.\n"
        summary += f"* **Total Chain Length:** {length} monomers.\n"
        if seq_type in ["DNA", "RNA"]:
            summary += f"* **GC Ratio:** {gc_content}% (Indicates structural stability and melting point characteristics).\n"
            summary += f"* **Transcription Output (RNA equivalent):** `{transcription[:50]}`{'...' if len(transcription) > 50 else ''}\n"
            summary += f"* **Predicted Translated Protein Chain:** `{protein_translation[:50]}`{'...' if len(protein_translation) > 50 else ''}\n"
        else:
            summary += "* **Note:** Detailed codon translation skipped as input format matches structural protein properties rather than open-reading nucleic frame blueprints."

        return {
            "success": True,
            "analysis": {
                "sequence_type": seq_type,
                "length": length,
                "gc_content": gc_content,
                "nucleotide_counts": counts,
                "summary": summary
            }
        }

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "online", "message": "Local MJ Biochemistry Analysis Engine is running flawlessly."}), 200

@app.route('/api/analyze-sequence', methods=['POST'])
def analyze_sequence_route():
    try:
        data = request.get_json()
        if not data or 'sequence' not in data:
            return jsonify({"success": False, "error": "No data sequence string provided to endpoint."}), 400
        
        engine = MJBiochemist()
        result = engine.analyze_sequence(data['sequence'])
        
        if result["success"]:
            return jsonify(result), 200
        return jsonify(result), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
