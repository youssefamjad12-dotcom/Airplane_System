import csv
import hashlib
import os
import uuid

ADMINS_FILE = "admins.csv"

class Admin:
    def __init__(self, username: str, password: str, name: str):
        self.admin_id = str(uuid.uuid4())
        self.username = username
        self.name = name
        self.password_hash = self._hash_password(password)

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

class AdminManager:
    def __init__(self, file_path=ADMINS_FILE):
        self.file_path = file_path
        self.admins = {}  # key: username, value: Admin instance
        self._load_admins()

    def _load_admins(self):
        if not os.path.exists(self.file_path):
            return
        with open(self.file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                admin = Admin(row["username"], row["password_hash"], row["name"])
                admin.admin_id = row["admin_id"]
                admin.password_hash = row["password_hash"]  # already hashed
                self.admins[admin.username] = admin

    def _save_admins(self):
        with open(self.file_path, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["admin_id", "username", "name", "password_hash"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for admin in self.admins.values():
                writer.writerow({
                    "admin_id": admin.admin_id,
                    "username": admin.username,
                    "name": admin.name,
                    "password_hash": admin.password_hash
                })

    def add_admin(self, username, password, name):
        if username in self.admins:
            print("Username already exists")
            return None
        admin = Admin(username, password, name)
        self.admins[username] = admin
        self._save_admins()
        print(f"Admin {username} added successfully")
        return admin

    def login(self, username, password):
        admin = self.admins.get(username)
        if not admin:
            print("Invalid username")
            return None
        if admin.password_hash != hashlib.sha256(password.encode()).hexdigest():
            print("Invalid password")
            return None
        print(f"Admin {username} logged in successfully")
        return admin
