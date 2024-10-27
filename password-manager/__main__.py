import argparse, sys

from sqlalchemy import select
from sqlalchemy.orm import Session

from .generate_password import hashPassword
from .database import Database, Account, decrypt, encrypt

parser = argparse.ArgumentParser("Password Generator")

parser.add_argument("--version", action='version', version="%(prog)s 0.1")
parser.add_argument("--length", default=12, type=int, help="The minimal length the password should be")
    
args = parser.parse_args()

password = "password"
hashedpassword, salt = hashPassword(password)

db = Database()

db.createAccount(Account(
    email='email',
    password=hashedpassword,
    salt=salt,
))

db.createAccount(Account(
    email='email',
    password=hashedpassword,
    salt=salt,
))

with Session(db.engine) as session:
    stmt = select(Account).where(Account.salt.is_(salt))

    if account := session.scalar(stmt):
        print(f"Password: {password}")
        print(f"Salt: {salt}")
        print(f"Hash: {hashedpassword}")

        encrypted = encrypt(password, account.salt)

        print(encrypted)
        print(decrypt(encrypted, account.salt))
