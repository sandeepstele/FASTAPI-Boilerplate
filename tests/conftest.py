import sys
import os

# Ensure project root is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Use an in-memory SQLite database for tests to avoid state leakage
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
