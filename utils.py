# MJ - Biochemistry AI Tool
# Utility Functions

import os
import json
from datetime import datetime

def log_message(message, level="INFO"):
    """Log messages with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {level}: {message}")

def read_fasta_file(file_path):
    """Read FASTA sequence file"""
    sequences = {}
    current_id = None
    current_seq = ""
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('>'):
                    if current_id:
                        sequences[current_id] = current_seq
                    current_id = line[1:]
                    current_seq = ""
                else:
                    current_seq += line
            
            if current_id:
                sequences[current_id] = current_seq
        
        log_message(f"Read {len(sequences)} sequences from {file_path}")
        return sequences
    
    except Exception as e:
        log_message(f"Error reading FASTA file: {str(e)}", "ERROR")
        return None

def save_json(data, file_path):
    """Save data as JSON file"""
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        log_message(f"Saved JSON to {file_path}")
        return True
    except Exception as e:
        log_message(f"Error saving JSON: {str(e)}", "ERROR")
        return False

def load_json(file_path):
    """Load JSON file"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        log_message(f"Error loading JSON: {str(e)}", "ERROR")
        return None

def validate_sequence(sequence):
    """Validate DNA/RNA/Protein sequence"""
    dna_chars = set('ATGC')
    rna_chars = set('AUGC')
    protein_chars = set('ACDEFGHIKLMNPQRSTVWY')
    
    seq_upper = sequence.upper().replace('-', '').replace('N', '')
    
    if all(c in dna_chars for c in seq_upper):
        return "DNA"
    elif all(c in rna_chars for c in seq_upper):
        return "RNA"
    elif all(c in protein_chars for c in seq_upper):
        return "PROTEIN"
    else:
        return "UNKNOWN"

if __name__ == "__main__":
    log_message("Utils module loaded successfully")
