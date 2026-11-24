from getpass import getpass
from werkzeug.security import generate_password_hash
from db import q

name = input("Admin name: ").strip()
email = input("Admin email: ").strip().lower()
pw = getpass("Admin password (min 6 chars): ")
if len(pw) < 6:
    raise SystemExit("Password too short.")
q("INSERT INTO admins (name,email,password_hash) VALUES (%s,%s,%s)",
  (name, email, generate_password_hash(pw)), commit=True)
print("Admin created. You can now log in as Admin.")
