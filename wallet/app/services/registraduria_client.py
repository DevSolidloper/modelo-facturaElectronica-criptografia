#wallet/app/services/registraduria_client.py
import httpx
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

REG_URL = "http://localhost:8000/public-key"

def obtener_public_key():
    response = httpx.get(REG_URL)
    data = response.json()
    pk_bytes = bytes.fromhex(data["public_key"])

    return Ed25519PublicKey.from_public_bytes(pk_bytes)