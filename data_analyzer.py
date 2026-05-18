# MJ - Biochemistry AI Tool
# Data Analyzer Module

import csv
import json
from utils import log_message

class DataAnalyzer:
    """Analyze experimental data from CSV/Excel files"""
    
    def __init__(self, data=None):
        self.data = data or []
    
    def load_csv(self, file_path):
        """Load data from CSV file"""
        try:
            with open(file_path, 'r') as f:
                reader = csv.DictReader(f)
                self.data = list(reader)
            log_message(f"Loaded {len(self.data)} rows from CSV")
            return True
        except Exception as e:
            log_message(f"Error loading CSV: {str(e)}", "ERROR")
            return False
    
    def get_summary_statistics(self, column):
        """Calculate summary statistics for a column"""
        try:
            values = [float(row[column]) for row in self.data if row.get(column)]
            
            if not values:
                return None
            
            stats = {
                "count": len(values),
                "mean": round(sum(values) / len(values), 2),
                "min": min(values),
                "max": max(values),
                "sum": round(sum(values), 2)
            }
            
            return stats
        except Exception as e:
            log_message(f"Error calculating statistics: {str(e)}", "ERROR")
            return None
    
    def find_outliers(self, column, threshold=2.0):
        """Find outliers in data using standard deviation"""
        try:
            values = [float(row[column]) for row in self.data if row.get(column)]
            
            if len(values) < 3:
                return []
            
            mean = sum(values) / len(values)
            variance = sum((x - mean) ** 2 for x in values) / len(values)
            std_dev = variance ** 0.5
            
            outliers = []
            for i, row in enumerate(self.data):
                try:
                    val = float(row[column])
                    if abs((val - mean) / std_dev) > threshold:
                        outliers.append({"index": i, "value": val})
                except:
                    pass
            
            log_message(f"Found {len(outliers)} outliers")
            return outliers
        
        except Exception as e:
            log_message(f"Error finding outliers: {str(e)}", "ERROR")
            return []
    
    def get_data_summary(self):
        """Get overall data summary"""
        summary = {
            "total_rows": len(self.data),
            "columns": list(self.data[0].keys()) if self.data else [],
            "data_preview": self.data[:5] if self.data else []
        }
        return summary
    
    def export_json(self, file_path):
        """Export data as JSON"""
        try:
            with open(file_path, 'w') as f:
                json.dump(self.data, f, indent=2)
            log_message(f"Exported data to {file_path}")
            return True
        except Exception as e:
            log_message(f"Error exporting JSON: {str(e)}", "ERROR")
            return False

if __name__ == "__main__":
    # Test
    analyzer = DataAnalyzer()
    print("Data Analyzer module loaded successfully")
