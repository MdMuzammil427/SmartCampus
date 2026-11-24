import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = "change-this-to-a-long-random-string"
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "YOUR_MYSQL_PASSWORD"   # <-- type your real password here
DB_NAME = "smartcampus_db"
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 MB upload limit
