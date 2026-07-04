import httpx
from cryptography.hazmat.primitives import serialization


DIAN_URL = "http://localhost:8002/public-key"


def obtener_public_key_dian():
    response = httpx.get(DIAN_URL)
    pem = response.json()["public_key"]

    return serialization.load_pem_public_key(pem.encode())