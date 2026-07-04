import json


def firmar_factura(private_key, factura: dict):
    data = json.dumps(factura, sort_keys=True).encode("utf-8")
    return private_key.sign(data).hex()