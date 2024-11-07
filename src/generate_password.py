import random, string

rng = random.SystemRandom()

def generatePassword(minimumCharacters):
    "Generate a random password thats at least {minimumCharacters} long"

    Characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(rng.choice(Characters) for _ in range(0, minimumCharacters))
