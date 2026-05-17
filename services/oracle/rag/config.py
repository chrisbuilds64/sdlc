import os
from dotenv import load_dotenv

load_dotenv()

ORACLE_HOST = os.getenv("ORACLE_HOST", "localhost")
ORACLE_PORT = int(os.getenv("ORACLE_PORT", "1521"))
ORACLE_PDB  = os.getenv("ORACLE_PDB", "ENTW")
ORACLE_USER = os.getenv("ORACLE_USER", "pdb_admin")
ORACLE_PASS = os.getenv("ORACLE_PASS", "OraclePdb2026")

EMBED_MODEL   = os.getenv("EMBED_MODEL", "all-MiniLM-L6-v2")
OLLAMA_HOST   = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL  = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:14b")

CHUNK_SIZE    = int(os.getenv("CHUNK_SIZE", "400"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
TOP_K         = int(os.getenv("TOP_K", "5"))

SOURCE_FILTER = os.getenv("SOURCE_FILTER", "")
