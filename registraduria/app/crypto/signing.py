import json

def firmar_credencial(private_key, credential: dict):
    data = json.dumps(credential, sort_keys=True).encode('utf-8')
    firma = private_key.sign(data)
    return firma.hex()