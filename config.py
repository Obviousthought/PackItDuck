import os
# from views import app

# Config file, put all your keys and passwords and whatnot in here
DB_URI = os.environ.get("DATABASE_URL", "sqlite:///packinglist.db")
# DB_URI = os.environ.get("DATABASE_URL", "postgresql:///packinglist.db")
SECRET_KEY = "this should be a secret"

# db = DB_URI(app)