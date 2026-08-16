import os

from dotenv import load_dotenv


load_dotenv()

API_VERSION = os.getenv("API_VERSION")
DATABASE_URL = os.getenv("DATABASE_URL")
SHOW_SQL = os.getenv("SHOW_SQL", True)
JWT_SECRET = os.getenv("JWT_SECRET")
ALGO = os.getenv("ALGO", "HS256")
ADMIN_NAME = os.getenv("ADMIN_NAME")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
MODEL_PATH = os.getenv("MODEL_PATH")