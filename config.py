# MJ - Biochemistry AI Tool
# Configuration File

import os

# App Settings
APP_NAME = "MJ - Biochemistry AI Tool"
APP_VERSION = "1.0.0"
DEBUG = True

# Database
DATABASE_FILE = "mj_database.db"

# Features
FEATURES = {
    "sequence_analyzer": True,
    "data_analyzer": True,
    "report_generator": True,
    "protocol_search": False,  # Coming soon
    "literature_search": False  # Coming soon
}

# API Keys (empty for now)
API_KEYS = {
    "ncbi": "",
    "uniprot": "",
    "pubmed": ""
}

# Supported file types
SUPPORTED_FILES = {
    "sequences": [".fasta", ".fa", ".txt"],
    "data": [".csv", ".xlsx", ".xls"],
    "images": [".jpg", ".png", ".tiff"],
    "documents": [".pdf", ".txt", ".doc"]
}

# Print config on load
if DEBUG:
    print(f"🚀 {APP_NAME} v{APP_VERSION}")
    print(f"Debug mode: {DEBUG}")
    print(f"Database: {DATABASE_FILE}")
