# =============================================================================
# Configuration file for RAG Assistant
# =============================================================================
# Why a config file? 
# - Change settings in ONE place, not scattered across files
# - Easy to adjust for different environments (your laptop vs. server)
# - No "magic numbers/variables" buried in code
# =============================================================================

import os

# Default Configuration
DEFAULT_DB_PATH = "backend/war_vector.duckdb" # UPDATE WITH YOUR .duckdb file for database.py
DEFAULT_TOP_K = 10 # Default top k neighbors parameter for app.py
DEFAULT_MAX_ITER = 3 # Default iterations for app.py
DEFAULT_MODEL = "gpt-4o-mini" # Default model for app.py

# Model Options
AVAILABLE_MODELS = ["gpt-4o-mini"] # List of all available models for app.py

# Embedding Model
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2" # UPDATE TO YOUR MODEL
EMBEDDING_DIMENSION = 384  # UPDATE TO YOUR MODEL