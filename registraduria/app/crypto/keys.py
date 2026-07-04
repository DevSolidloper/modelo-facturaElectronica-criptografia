from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from pathlib import Path

from shared.key_manager import guardar_private_key, guardar_public_key, cargar_private_key, cargar_public_key

PRIVATE = Path("keys/private.pem")
PUBLIC = Path("keys/public.pem")


def cargar_o_generar_claves():
    if PRIVATE.exists() and PUBLIC.exists():

        print("Cargando claves existentes...")

        return (
            cargar_private_key(PRIVATE),
            cargar_public_key(PUBLIC)
        )

    print("Generando nuevas claves...")
    
    private = Ed25519PrivateKey.generate()
    public = private.public_key()
    
    guardar_private_key(private, PRIVATE)
    guardar_public_key(public, PUBLIC)

    return private, public