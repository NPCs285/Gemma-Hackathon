from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


load_dotenv()


def load_env(key, default):
    return os.getenv(key, default)


def get_db_url():
    DB_USER = load_env("DB_USER", "postgres")
    DB_PASSWORD = load_env("DB_PASSWORD", "postgres")
    DB_HOST = load_env("DB_HOST", "localhost")
    DB_PORT = load_env("DB_PORT", "5432")
    DB_NAME = load_env("DB_NAME", "tracker")

    return f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def create_db_conn():
    DATABASE_URL = get_db_url()
    engine = create_engine(DATABASE_URL, echo=True)
    conn = engine.connect()
    return conn
