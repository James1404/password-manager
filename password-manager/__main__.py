import argparse

from .generate_password import hashPassword
from .database import Database, Account
from .ui import PasswordManagerApp

def main():
    parser = argparse.ArgumentParser("Password Generator")

    parser.add_argument("--version", action='version', version="%(prog)s 0.1")
    parser.add_argument("--length", default=12, type=int, help="The minimal length the password should be")
    
    args = parser.parse_args()

    password = "Jamesb99"
    hashedpassword, salt = hashPassword(password)

    db = Database()

    james = Account(
        email='jamesbarnfather99@gmail.com',
        password=hashedpassword,
        salt=salt,
    )

    db.createAccount(james)
    
    print(f"Password: {password}")
    print(f"Salt: {salt}")
    print(f"Hash: {hashedpassword}")

    app = PasswordManagerApp()
    app.run()

if __name__ == "__main__":
    main()
