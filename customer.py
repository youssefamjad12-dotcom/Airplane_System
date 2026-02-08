import csv
import hashlib
import os

class Customer:
    FILENAME = "users.csv"

    def __init__(self, name="", email="", role="customer"):
        self.name = name
        self.email = email
        self.role = role

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @classmethod
    def ensure_file(cls):
        if not os.path.exists(cls.FILENAME):
            with open(cls.FILENAME, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["name", "email", "password_hash", "role"])

    @classmethod
    def register(cls, name, email, password, role="customer"):
        cls.ensure_file()

        # التحقق من وجود ايميل مسبقًا
        with open(cls.FILENAME, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["email"].lower() == email.lower():
                    print("Already registered with this email.")
                    return None

        pwd_hash = cls.hash_password(password)

        with open(cls.FILENAME, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([name, email, pwd_hash, role])

        print("Registered Successfully.")
        return cls(name, email, role)

    @classmethod
    def login(cls, email, password):
        cls.ensure_file()
        pwd_hash = cls.hash_password(password)

        with open(cls.FILENAME, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["email"].lower() == email.lower() and row["password_hash"] == pwd_hash:
                    print(f"Login Successfully by: {row['role']}")
                    return cls(row["name"], row["email"], row["role"])

        print("Wrong email or password.")
        return None
