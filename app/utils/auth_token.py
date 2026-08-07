from typing import Any

import jwt

from app.utils import env


def encode_token(payload:dict[str, Any]):
    token = jwt.encode(payload, env.JWT_SECRET, algorithm=env.ALGO)

    return token

def decode_token(token:str):
    payload = jwt.decode(token, env.JWT_SECRET, algorithms=env.ALGO)
    return payload
