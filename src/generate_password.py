import hashlib
import random

from functools import reduce
import secrets
import string

from cryptography.fernet import Fernet

rng = random.SystemRandom()

def replaceWithEquivalent(c: str) -> str:
    """Replace the provided character with a character that looks somewhat similar

    For e.g. replace 'A' with '@'
    Or 'I' with '1'
    """
    equivalent = {
        'a': ['@'],
        'i': ['1','!'],
        'o': ['0'],
        'l': ['1'],
    }

    return rng.choice(equivalent.get(c, c))

def loadDictionary(filepath: str) -> list[str]:
    """Return's a list of english words loaded from a file, each line in the file contains a single word"""
    with open(filepath) as file:
        return [line.strip() for line in file]

def generatePassword(minimumCharacters):
    """Generate a random password thats at least {minimumCharacters} long

    combine some random words, and replace certain characters with equivalent characters.
    for e.g. replace 'A' with '@', or 'I' with '1'.

    i'll also append random numbers to the end of certain words.
    """
    
    # list from: https://www.ef.co.uk/english-resources/english-vocabulary/top-1000-words/
    words = loadDictionary('words.txt')

    chosen: list[str] = []

    chosenLen = lambda: reduce(lambda x, y: x + len(y), chosen, 0)
    while chosenLen() < minimumCharacters:
        chosen.append(rng.choice(words).capitalize())
        
    chosen = [''.join([replaceWithEquivalent(x) for x in word]) for word in chosen]

    allowedDelimiters = [ '-', '_', '']
    return reduce(lambda x, y: x + rng.choice(allowedDelimiters) + y, chosen)

Alphabet = string.ascii_letters + string.digits
SaltLength = 32

def hashPassword(password: str) -> tuple[bytes, bytes]:
    salt = Fernet.generate_key()
    return (
        hashlib.sha256(password.encode() + salt).digest(),
        salt
    )
