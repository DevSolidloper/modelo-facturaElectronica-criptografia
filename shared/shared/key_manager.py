from pathlib import Path

from cryptography.hazmat.primitives import serialization


def guardar_private_key(private_key, path: Path):

    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    path.write_bytes(pem)

def guardar_public_key(public_key, path: Path):

    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    path.write_bytes(pem)

def cargar_private_key(path: Path):

    return serialization.load_pem_private_key(
        path.read_bytes(),
        password=None
    )

def cargar_public_key(path: Path):

    return serialization.load_pem_public_key(
        path.read_bytes()
    )