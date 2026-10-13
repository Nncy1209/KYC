import os
from dotenv import load_dotenv

load_dotenv()

# ===============================
# Database
# ===============================

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ===============================
# API Keys
# ===============================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ===============================
# Upload Settings
# ===============================

UPLOAD_FOLDER = "uploads"
CAPTURE_FOLDER = "captures"
REPORT_FOLDER = "reports"

MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 10))

ALLOWED_EXTENSIONS = [
    "jpg",
    "jpeg",
    "png"
]