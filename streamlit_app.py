"""
Streamlit Community Cloud Deployment Entrypoint for InsurAgent.
Ensures seamless compatibility whether Streamlit Cloud is configured to look for
'streamlit_app.py' (default) or 'app.py'.
"""
import sys
try:
    __import__("pysqlite3")
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass

import runpy
runpy.run_path("app.py", run_name="__main__")
