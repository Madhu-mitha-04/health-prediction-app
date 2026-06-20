import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load variables from .env (if present) into os.environ
load_dotenv()


class Config:
    """Base configuration shared by all environments."""

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "health_prediction_db")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")

    # URL-encode the password so special characters (@, :, /, #, etc.)
    # don't get misinterpreted as part of the connection URL structure.
    _DB_PASSWORD_ENCODED = quote_plus(DB_PASSWORD)

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{_DB_PASSWORD_ENCODED}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Path to the trained scikit-learn model artifact
    ML_MODEL_PATH = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "ml", "model.pkl"
    )

    # CORS - allow the React dev server
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000")