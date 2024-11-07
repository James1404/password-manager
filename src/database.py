from dataclasses import dataclass
from sqlalchemy import ForeignKey, Text, create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, Mapped, mapped_column, registry, relationship

from typing import List

from cryptography.fernet import Fernet

import hashlib, hmac

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
        default_factory=list,
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
    account: Mapped[Account | None] = relationship(default=None)

LocalEncryptionKey = b'a local encryption key'

def getKey(salt: bytes) -> bytes:
    return salt + LocalEncryptionKey

def encrypt(input: str, key: bytes) -> bytes:
    f = Fernet(key)
    token = f.encrypt(input.encode())
    return token

def decrypt(input: bytes, key: bytes) -> str:
    f = Fernet(key)
    token = f.decrypt(input)
    return token.decode()

@dataclass
class AccountAuthenticationError(BaseException):
    msg: str

@dataclass
class Database(Session):
    engine = create_engine('sqlite+pysqlite:///passwords.db', echo=False)

    def __init__(self):
        super().__init__(self.engine, expire_on_commit=True)
        reg.metadata.create_all(self.engine)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def createAccount(self, email: str, password: str) -> Account | None:
        salt = Fernet.generate_key()
        hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)

        account = Account(email, hash, salt)

        try:
            self.add(account)
            self.commit()
        except IntegrityError:
            print("Account already exists")
            return None
            
        return account

    def authenticateAccount(self, email: str, password: str) -> Account:
        """Authenticate an account
        """

        stmt = select(Account).where(Account.email.is_(email))

        if result := self.scalar(stmt):
            if hmac.compare_digest(
                result.password,
                hashlib.pbkdf2_hmac('sha256', password.encode(), result.salt, 100000)
            ):
                return result

            raise AccountAuthenticationError("Password does not match")
        
        raise AccountAuthenticationError("Account does not exist")
