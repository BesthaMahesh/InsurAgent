"""
Streamlit Community Cloud Deployment Entrypoint for InsurAgent.
Ensures seamless compatibility whether Streamlit Cloud is configured to look for
'streamlit_app.py' (default) or 'app.py'.
"""
import sys
from pathlib import Path

# Linux SQLite patch for ChromaDB on Streamlit Cloud
try:
    __import__("pysqlite3")
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass

app_file = Path(__file__).resolve().parent / "app.py"
with open(app_file, "r", encoding="utf-8") as f:
    code = f.read()

exec(compile(code, str(app_file), "exec"), globals())
