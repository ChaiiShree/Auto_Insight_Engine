import os
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

# Load local environment variables for local development
load_dotenv()

class Config:
    """Cloud-ready centralized configuration management"""
    
    # 1. Secure API Key Handling
    # Checks Streamlit Secrets first (Cloud), then falls back to .env (Local)
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    # 2. Cross-Platform Path Handling
    # Streamlit Cloud uses a read-only filesystem; we must use /tmp for writing files
    IS_CLOUD = "STREAMLIT_SERVER_PORT" in os.environ
    
    if IS_CLOUD:
        BASE_DIR = Path("/tmp")
        # On Cloud, we don't need the parent.parent logic
        DATA_DIR = BASE_DIR / "data"
    else:
        BASE_DIR = Path(__file__).resolve().parent.parent
        DATA_DIR = BASE_DIR / "data"

    INPUT_DIR = DATA_DIR / "input"
    OUTPUT_DIR = DATA_DIR / "output"
    
    # Gemini Configuration
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2048"))
    
    # ML Model Configuration
    CONTAMINATION_FACTOR = float(os.getenv("CONTAMINATION_FACTOR", "0.1"))
    N_ESTIMATORS = int(os.getenv("N_ESTIMATORS", "100"))
    
    @classmethod
    def setup_directories(cls):
        """Ensure temporary processing directories exist"""
        cls.INPUT_DIR.mkdir(parents=True, exist_ok=True)
        cls.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
    @classmethod
    def validate(cls):
        """Validate critical configuration"""
        if not cls.GEMINI_API_KEY:
            # This error will show up in the Streamlit logs if secrets are missing
            raise ValueError("GEMINI_API_KEY not found. Please add it to Streamlit Secrets.")
        return True

# Setup directories automatically on import
Config.setup_directories()