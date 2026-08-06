import os

from dotenv import load_dotenv


load_dotenv()

API_VERSION = os.getenv("API_VERSION")
DATABASE_URL = os.getenv("DATABASE_URL")