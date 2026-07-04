import json
from cryptography.exceptions import InvalidSignature

def verificar_credencial(public_key, credencial: dict, firma_hex: str):

    try:
        data = json.dumps(credencial, sort_keys=True).encode("utf-8")
        firma = bytes.fromhex(firma_hex)

        public_key.verify(firma, data)
        return True
    
    except InvalidSignature:
        return False