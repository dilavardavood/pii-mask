import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default-key")
    DATABASE_URL = os.getenv("DATABASE_URL")
    OPENAI_API_KEY = os.getenv("OPENAI_KEY")
    BOT_TOKEN = '7578145894:AAFeJY4C5DwRXuc20oE01yIfs1t_uts5I9M'
