import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from app.models.factura import Factura


def verificar_firma_comercio(public_key, factura:Factura, firma_hex):
    try:
        data = json.dumps(
            factura.model_dump(), #se convierte el objeto factura a un diccionario
            sort_keys=True
        ).encode("utf-8")

        firma = bytes.fromhex(firma_hex)

        public_key.verify(firma, data)
        return True

    except InvalidSignature:
        return False