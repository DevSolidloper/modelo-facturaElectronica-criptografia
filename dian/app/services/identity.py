from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def resolver_token_fiscal(private_key, token_hex: str):

    token = bytes.fromhex(token_hex)

    cedula = private_key.decrypt(
        token,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return cedula.decode()