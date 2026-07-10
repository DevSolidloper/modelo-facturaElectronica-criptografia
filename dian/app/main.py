from fastapi import FastAPI, HTTPException

from app.crypto.keys import cargar_o_generar_claves
from cryptography.hazmat.primitives import serialization

from app.crypto.verify_comercio import verificar_firma_comercio
from app.services.identity import resolver_token_fiscal
from app.models.comercio import ComercioRegistro
from app.services.registro_comercios import registrar_comercio, obtener_public_key
from app.storage.comercios_db import COMERCIOS_DB

from app.models.factura import FacturaRequest


app = FastAPI()




SK_DIAN, PK_DIAN = cargar_o_generar_claves()



@app.get("/public-key")
def get_public_key():
    return {
        "public_key": PK_DIAN.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()
    }

@app.post("/registrar-comercio")
def registrar(payload: ComercioRegistro):
    registrar_comercio(payload.nit, payload.public_key)
    print(f"Comercio registrado: {payload.nit} con public key {payload.public_key}")
    return {
        "mensaje": "comercio registrado correctamente"
    }

@app.post("/recibir-factura")
def recibir_factura(payload: FacturaRequest):

    print(f"Factura recibida de comercio {payload.nit} con token fiscal {payload.factura.tokenFiscal} y total {payload.factura.total}")

    factura = payload.factura
    firma = payload.firmaEmpresa
    nit = payload.nit

    pk_empresa = obtener_public_key(nit)
    print(f"Public key del comercio {nit}: {pk_empresa}")

    if not pk_empresa:
        return {"error": "comercio no registrado"}
    
    valido = verificar_firma_comercio(pk_empresa, factura, firma)

    # 1. verificar firma del comercio
    if not valido:
        raise HTTPException(400, "Factura inválida")

    # 2. resolver identidad
    cedula = resolver_token_fiscal(SK_DIAN ,payload.factura.tokenFiscal)
    print(f"Factura recibida de comercio {nit} para contribuyente {cedula} con total {factura.total}")
    return {
        "estado": "aceptada",
        "contribuyente": cedula,
        "total": factura.total
    }

@app.get("/me")
def storage():
    return COMERCIOS_DB
