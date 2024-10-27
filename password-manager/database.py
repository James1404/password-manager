from dataclasses import dataclass
from sqlalchemy import ForeignKey, Text, create_engine, select
from sqlalchemy.orm import Session, Mapped, mapped_column, registry, relationship

from typing import List

from cryptography.fernet import Fernet

import hashlib

reg = registry()

@reg.mapped_as_dataclass
class Account:
    __tablename__ = "account_table"

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True,init=False)
    email: Mapped[str] = mapped_column(Text, nullable=False,unique=True)
    password: Mapped[bytes] = mapped_column(Text, nullable=False)
    salt: Mapped[bytes] = mapped_column(Text, nullable=False)

    items: Mapped[List["Item"]] = relationship(
        back_populates="account",
        default_factory=list
    )

@reg.mapped_as_dataclass
class Item:
    """An account item with encrpyted fields"""
    
    __tablename__ = "item_table"

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True,init=False)

    name: Mapped[bytes] = mapped_column(Text, nullable=False)
    url: Mapped[bytes] = mapped_column(Text, nullable=False)
    username: Mapped[bytes] = mapped_column(Text, nullable=False)
    password: Mapped[bytes] = mapped_column(Text, nullable=False)
    
    account_id: Mapped[int] = mapped_column(ForeignKey("account_table.id"))
    account: Mapped["Account"] = relationship(default=None)

def encrypt(input: str, key: bytes) -> bytes:
    f = Fernet(key)
    token = f.encrypt(input.encode())
    return token

def decrypt(input: bytes, key: bytes) -> str:
    f = Fernet(key)
    token = f.decrypt(input)
    return token.decode()

@dataclass
class Database:
    engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)

    def __init__(self) -> None:
        reg.metadata.create_all(self.engine)

    def createAccount(self, account: Account):
        try:
            with Session(self.engine) as session:
                session.add_all([account])
                session.commit()

                return True
        except:
            return False
            
    def authenticatePassword(self, email: str, password: str) -> bool:
        """Authenticate an account
        """

        with Session(self.engine) as session:
            stmt = select(Account).where(Account.email.is_(email))

            if result := session.scalar(stmt):
                hash = hashlib.sha256(password.encode() + result.salt)
                return hash == result.password

            return False
