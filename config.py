import os
from dotenv import load_dotenv

load_dotenv()

print("HOST:", os.getenv("MYSQL_HOST"))
print("USER:", os.getenv("MYSQL_USER"))
print("PASSWORD:", os.getenv("MYSQL_PASSWORD"))
print("DB:", os.getenv("MYSQL_DB"))

class Config:
    SECRET_KEY = "grocery-secret-key"

    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB = os.getenv("MYSQL_DB")