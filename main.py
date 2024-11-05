import os
import argparse, sys, getpass
from cmd import Cmd
from typing import IO

from sqlalchemy import select
from sqlalchemy.orm import Session

from dotenv import dotenv_values, load_dotenv

from src.database import AccountAuthenticationError, Database, Account, Item, decrypt, encrypt

class AccountInterpreter(Cmd):
    def __init__(self, session: Session, account: Account, completekey: str = "tab", stdin: IO[str] | None = None, stdout: IO[str] | None = None) -> None:
        super().__init__(completekey, stdin, stdout)
        self.session = session
        self.account = account
        self.prompt = f"({self.account.email}) "

    def do_logout(self, _):
        "Logout the current account"
        return True

    def do_get_items(self, _):
        print(self.account.id)
        stmt = select(Item).where(Item.account_id.is_(self.account.id))

        items = self.session.scalars(stmt)

        for item in items:
            print(item)


class MainInterpreter(Cmd):
    intro = "Create an account with the 'create_account' command; or login with the 'login' command"
    prompt = "(Getting Started) "
    
    db: Database = Database()
    
    def do_quit(self, _):
        "Quit the app"
        return True

    def do_exit(self, _):
        "Exit the app"
        return True

    def do_close(self, _):
        "Close the app"
        return True

    def do_login(self, _):
        "Login to an account"
        email = input("Email: ")
        password = getpass.getpass("Password: ")

        with Session(self.db.engine) as session:
            try:
                account = self.db.authenticateAccount(session, email, password)
                print("Successfully logged in")
                
                AccountInterpreter(session, account).cmdloop()
            except AccountAuthenticationError as exc:
                print(exc)

    def do_create_account(self, _):
        "Create a new account with an email and password"
        email = input("Email: ")
        password = getpass.getpass("Password: ")

        with Session(self.db.engine) as session:
            account = self.db.createAccount(session, email, password)

            AccountInterpreter(self.db, account).cmdloop()

    def do_get_accounts(self, _):
        "Get all registered accounts via their email"
        with Session(self.db.engine) as session:
            stmt = select(Account)
            accounts = session.scalars(stmt)
            for account in accounts:
                print(account.email)

    def do_delete_account(self, _):
        "Delete an account via it's email: delete_account exampleEmail@gmail.com"

        email = input("Email: ")

        with Session(self.db.engine) as session:
            print(f"Deleting '{email}' account")
            session.query(Account).where(Account.email.is_(email)).delete()
            session.commit()

    def do_reset(self, _):
        "Delete all accounts and their bound items"
        with Session(self.db.engine) as session:
            print("Resetting databse")
            session.query(Account).delete()
            session.query(Item).delete()
            session.commit()  

def main():
    app = MainInterpreter()
    app.cmdloop()

if __name__ == "__main__":
    main()
