import os

from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = "postgres://postgres:postgres@localhost:5432/contest"
REDIS_URL = "redis://localhost:6380/0"
