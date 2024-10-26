import argparse, sys

from .generate_password import hashPassword
from .database import Database, Account, encrypt

parser = argparse.ArgumentParser("Password Generator")

parser.add_argument("--version", action='version', version="%(prog)s 0.1")
parser.add_argument("--length", default=12, type=int, help="The minimal length the password should be")
    
args = parser.parse_args()

password = "password"
hashedpassword, salt = hashPassword(password)

db = Database()

james = Account(
    email='email',
    password=hashedpassword,
    salt=salt,
)

db.createAccount(james)
    
print(f"Password: {password}")
print(f"Salt: {salt}")
print(f"Hash: {hashedpassword}")

print(encrypt(hashedpassword, password))
