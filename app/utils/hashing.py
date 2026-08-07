import hashlib

from pwdlib import PasswordHash


password_hasher = PasswordHash.recommended()

def hash_password(password:str):
    return password_hasher.hash(password)

def verify_password(password:str, hashed:str):
    return password_hasher.verify(password, hashed)

def hash_api_key(api_key:str):
    return hashlib.sha256(
        api_key.encode("utf-8")
    ).hexdigest()