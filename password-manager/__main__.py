import os
import argparse, sys

from sqlalchemy import select
from sqlalchemy.orm import Session

from dotenv import load_dotenv

from .generate_password import hashPassword
from .database import Database, Account, Item, decrypt, encrypt

def main():
    parser = argparse.ArgumentParser("Password Generator")

    parser.add_argument("--version", action='version', version="%(prog)s 0.1")
    parser.add_argument("--length", default=12, type=int, help="The minimal length the password should be")

    parser.add_argument("type", choices=['tui', 'gui'])
    
    args = parser.parse_args()

    load_dotenv()

    email = os.environ["TEST_EMAIL"]
    password = os.environ["TEST_PASSWORD"]
    hashedpassword, salt = hashPassword(password)

    db = Database()

    james = Account(
        email=email,
        password=hashedpassword,
        salt=salt,
    )
    james.items.append(Item(
        name=encrypt("google", james.salt),
        url=encrypt("www.google.com", james.salt),
        username=encrypt(email, james.salt),
        password=encrypt(password, james.salt),
        account=james,
        account_id=james.id,
    ))
    db.createAccount(james)
        
    db.createAccount(Account(
        email=email,
        password=hashedpassword,
        salt=salt,
    ))

    with Session(db.engine) as session:
        stmt = select(Account).where(Account.salt.is_(salt))
        
        if account := session.scalar(stmt):
            print(f"Password: {password}")
            print(f"Salt: {salt}")
            print(f"Hash: {hashedpassword}")

            print(encrypted := encrypt(password, account.salt))
            print(decrypt(encrypted, account.salt))

    match args.type:
        case 'gui':
            from .gui import GUI
            app = GUI()
            sys.exit(app.exec())
        case 'tui':
            from .tui import PasswordManagerApp
            app = PasswordManagerApp()
            app.run()

if __name__ == "__main__":
    main()
