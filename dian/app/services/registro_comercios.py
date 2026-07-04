from app.storage.comercios_db import COMERCIOS_DB
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey


def registrar_comercio(nit: str, public_key:str):
    COMERCIOS_DB[nit] = public_key
    return True


def obtener_public_key(nit: str):
    pk_hex = COMERCIOS_DB.get(nit)

    if pk_hex is None:
        return None

    return Ed25519PublicKey.from_public_bytes(
        bytes.fromhex(pk_hex)
    )