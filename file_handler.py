# MJ - Biochemistry AI Tool
# File Handler Module

import os
import json
import csv
from utils import log_message, read_fasta_file

class FileHandler:
    """Handle file uploads and processing"""
    
    UPLOAD_FOLDER = "uploads"
    MAX_FILE_SIZE = 52428800  # 50MB
    
    ALLOWED_EXTENSIONS = {
        'sequences': ['.fasta', '.fa', '.txt'],
        'data': ['.csv', '.xlsx', '.xls'],
        'images': ['.jpg', '.png', '.tiff'],
    }
    
    @staticmethod
    def ensure_upload_folder():
        """Create upload folder if it doesn't exist"""
        if not os.path.exists(FileHandler.UPLOAD_FOLDER):
            os.makedirs(FileHandler.UPLOAD_FOLDER)
            log_message(f"Created upload folder: {FileHandler.UPLOAD_FOLDER}")
    
    @staticmethod
    def is_allowed_file(filename, file_type):
        """Check if file type is allowed"""
        if file_type not in FileHandler.ALLOWED_EXTENSIONS:
            return False
        
        ext = os.path.splitext(filename)[1].lower()
        return ext in FileHandler.ALLOWED_EXTENSIONS[file_type]
    
    @staticmethod
    def save_uploaded_file(file_content, filename, file_type):
        """Save uploaded file"""
        try:
            FileHandler.ensure_upload_folder()
            
            if not FileHandler.is_allowed_file(filename, file_type):
                return {"success": False, "error": "File type not allowed"}
            
            filepath = os.path.join(FileHandler.UPLOAD_FOLDER, filename)
            
            with open(filepath, 'w') as f:
                f.write(file_content)
            
            log_message(f"File saved: {filename}")
            return {"success": True, "filepath": filepath}
        
        except Exception as e:
            log_message(f"Error saving file: {str(e)}", "ERROR")
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def read_fasta(filename):
        """Read FASTA file"""
        try:
            filepath = os.path.join(FileHandler.UPLOAD_FOLDER, filename)
            sequences = read_fasta_file(filepath)
            return {"success": True, "sequences": sequences}
        except Exception as e:
            log_message(f"Error reading FASTA: {str(e)}", "ERROR")
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def read_csv(filename):
        """Read CSV file"""
        try:
            filepath = os.path.join(FileHandler.UPLOAD_FOLDER, filename)
            data = []
            
            with open(filepath, 'r') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            
            log_message(f"Read {len(data)} rows from CSV")
            return {"success": True, "data": data, "rows": len(data)}
        
        except Exception as e:
            log_message(f"Error reading CSV: {str(e)}", "ERROR")
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def list_uploaded_files():
        """List all uploaded files"""
        try:
            FileHandler.ensure_upload_folder()
            files = os.listdir(FileHandler.UPLOAD_FOLDER)
            return {"success": True, "files": files}
        except Exception as e:
            log_message(f"Error listing files: {str(e)}", "ERROR")
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def delete_file(filename):
        """Delete uploaded file"""
        try:
            filepath = os.path.join(FileHandler.UPLOAD_FOLDER, filename)
            
            if os.path.exists(filepath):
                os.remove(filepath)
                log_message(f"File deleted: {filename}")
                return {"success": True}
            
            return {"success": False, "error": "File not found"}
        
        except Exception as e:
            log_message(f"Error deleting file: {str(e)}", "ERROR")
            return {"success": False, "error": str(e)}

if __name__ == "__main__":
    print("File Handler module loaded successfully")
