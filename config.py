from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "resume-score-analyzer-secret")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'instance' / 'app.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    UPLOAD_FOLDER = BASE_DIR / "uploads"
    GRAPH_FOLDER = BASE_DIR / "app" / "static" / "graphs"
    ALLOWED_PDF = {"pdf"}
    ALLOWED_IMAGE = {"png", "jpg", "jpeg", "webp"}