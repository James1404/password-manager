from dataclasses import dataclass
from sqlalchemy import ForeignKey, Text, create_engine, select
from sqlalchemy.orm import Session, Mapped, mapped_column, registry, relationship

import string, secrets

from typing import List

from cryptography.fernet import Fernet

import hashlib

reg = registry()

@reg.mapped_as_dataclass
class Account:
    __tablename__ = "account_table"

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True,init=False)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    salt: Mapped[str] = mapped_column(Text, nullable=False)

    items: Mapped[List["Item"]] = relationship(
        back_populates="account",
        default_factory=list
    )

@reg.mapped_as_dataclass
class Item:
    __tablename__ = "item_table"

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True,init=False)

    name: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    username: Mapped[str] = mapped_column(Text, nullable=False)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    
    account_id: Mapped[int] = mapped_column(ForeignKey("account_table.id"))
    account: Mapped["Account"] = relationship(default=None)
    

def authenticatePassword(session: Session, email: str, password: str) -> bool:
    """Authenticate an account
    """
    stmt = select(Account).where(Account.email.is_(email))

    result = session.scalar(stmt);

    if result:
        hash = hashlib.sha256((password + result.salt).encode()).hexdigest()

        return hash == result.password

    return False

def encrypt(input: str, key: str) -> str:
    f = Fernet(key)
    token = f.encrypt(input.encode())
    return token.decode()

@dataclass
class Database:
    engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)

    reg.metadata.create_all(engine)

    def createAccount(self, account: Account):
        with Session(self.engine) as session:
            session.add_all([account])
            session.commit()
