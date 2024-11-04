import os
import argparse, sys

from sqlalchemy import select
from sqlalchemy.orm import Session

from dotenv import load_dotenv

from src.database import Database, Account, Item, decrypt, encrypt

from cmd import Cmd

class MainCmd(Cmd):
    prompt = "> "

    db: Database = Database()

    def help_login(self):
        print("Login to an account with a email and password")

    def do_login(self, args):
        email, password = args.rsplit(" ", 1)

        if self.db.authenticatePassword(email, password):
            print("Success")
        else:
            print("Failed to login")

    def do_create_account(self, args):
        email, password = args.rsplit(" ", 1)

        self.db.createAccount(email, password)

    def do_get_accounts(self, args):
        with Session(self.db.engine) as session:
            stmt = select(Account)
            for account in (accounts := session.scalars(stmt)):
                print(account.email)

    def help_delete_account(self):
        print("Delete an account with the provided email")

    def do_delete_account(self, args):
        email = args

        with Session(self.db.engine) as session:
            print(f"Deleting '{email}' account")
            session.query(Account).where(Account.email.is_(email)).delete()
            session.commit()

def main():
    load_dotenv()

    app = MainCmd()
    app.cmdloop("Enter a command.")

if __name__ == "__main__":
    main()
