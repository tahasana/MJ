# MJ - Biochemistry AI Tool
# Sequence Analyzer Module

from utils import log_message, validate_sequence

class SequenceAnalyzer:
    """Analyze DNA, RNA, and Protein sequences"""
    
    def __init__(self, sequence):
        self.sequence = sequence.upper()
        self.seq_type = validate_sequence(sequence)
    
    def get_length(self):
        """Get sequence length"""
        return len(self.sequence)
    
    def get_gc_content(self):
        """Calculate GC content (for DNA/RNA)"""
        if self.seq_type not in ["DNA", "RNA"]:
            return None
        
        gc_count = self.sequence.count('G') + self.sequence.count('C')
        gc_percent = (gc_count / len(self.sequence)) * 100
        return round(gc_percent, 2)
    
    def count_nucleotides(self):
        """Count nucleotides"""
        counts = {
            'A': self.sequence.count('A'),
            'T': self.sequence.count('T'),
            'G': self.sequence.count('G'),
            'C': self.sequence.count('C'),
            'U': self.sequence.count('U')
        }
        return counts
    
    def count_amino_acids(self):
        """Count amino acids"""
        if self.seq_type != "PROTEIN":
            return None
        
        aa_counts = {}
        for aa in set(self.sequence):
            aa_counts[aa] = self.sequence.count(aa)
        return aa_counts
    
    def get_analysis_summary(self):
        """Get complete analysis summary"""
        summary = {
            "sequence_type": self.seq_type,
            "length": self.get_length(),
            "gc_content": self.get_gc_content(),
        }
        
        if self.seq_type in ["DNA", "RNA"]:
            summary["nucleotide_counts"] = self.count_nucleotides()
        elif self.seq_type == "PROTEIN":
            summary["amino_acid_counts"] = self.count_amino_acids()
        
        log_message(f"Analysis complete for {self.seq_type} sequence")
        return summary

if __name__ == "__main__":
    # Test
    test_seq = "ATGCATGCATGC"
    analyzer = SequenceAnalyzer(test_seq)
    print(analyzer.get_analysis_summary())
