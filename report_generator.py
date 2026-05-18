# MJ - Biochemistry AI Tool
# Report Generator Module

import json
from datetime import datetime
from utils import log_message

class ReportGenerator:
    """Generate analysis reports"""
    
    def __init__(self, title, analysis_type):
        self.title = title
        self.analysis_type = analysis_type
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.sections = []
    
    def add_section(self, heading, content):
        """Add a section to the report"""
        section = {
            "heading": heading,
            "content": content
        }
        self.sections.append(section)
        return self
    
    def add_data_table(self, heading, data):
        """Add a data table to the report"""
        section = {
            "heading": heading,
            "type": "table",
            "data": data
        }
        self.sections.append(section)
        return self
    
    def add_summary(self, summary_dict):
        """Add summary section"""
        self.add_section("Summary", summary_dict)
        return self
    
    def generate_text_report(self):
        """Generate plain text report"""
        report = f"""
{'='*60}
{self.title}
{'='*60}

Analysis Type: {self.analysis_type}
Generated: {self.created_at}

{'='*60}
"""
        for section in self.sections:
            report += f"\n{section['heading']}\n"
            report += "-" * 40 + "\n"
            
            if isinstance(section['content'], dict):
                for key, value in section['content'].items():
                    report += f"{key}: {value}\n"
            else:
                report += f"{section['content']}\n"
        
        report += f"\n{'='*60}\n"
        return report
    
    def generate_json_report(self):
        """Generate JSON report"""
        report_data = {
            "title": self.title,
            "analysis_type": self.analysis_type,
            "created_at": self.created_at,
            "sections": self.sections
        }
        return json.dumps(report_data, indent=2)
    
    def save_report(self, file_path, format_type="text"):
        """Save report to file"""
        try:
            if format_type == "text":
                content = self.generate_text_report()
            elif format_type == "json":
                content = self.generate_json_report()
            else:
                content = self.generate_text_report()
            
            with open(file_path, 'w') as f:
                f.write(content)
            
            log_message(f"Report saved to {file_path}")
            return True
        
        except Exception as e:
            log_message(f"Error saving report: {str(e)}", "ERROR")
            return False

if __name__ == "__main__":
    # Test
    report = ReportGenerator("Test Report", "Sequence Analysis")
    report.add_section("Introduction", "This is a test report")
    report.add_summary({"Status": "Success", "Items": 5})
    print(report.generate_text_report())
