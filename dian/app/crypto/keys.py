from cryptography.hazmat.primitives.asymmetric import rsa
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

    private = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public = private.public_key()

    guardar_private_key(private, PRIVATE)
    guardar_public_key(public, PUBLIC)

    return private, public