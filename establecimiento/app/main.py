from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx

from app.models.factura import FacturaRequest
from app.crypto.signing import firmar_factura

from app.crypto.keys import generar_o_cargar_claves

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives import serialization

SK_EMPRESA, PK_EMPRESA = generar_o_cargar_claves()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/registrar-en-dian")
def registrar_en_dian():
    public_key_bytes = PK_EMPRESA.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    payload = {
        "nit": "900123456",
        "public_key": public_key_bytes.hex()
    }

    response = httpx.post(
        "http://localhost:8002/registrar-comercio",
        json=payload
    )

    return response.json()


@app.post("/facturar")
def facturar(req: FacturaRequest):

    factura = {
        "tokenFiscal": req.tokenFiscal,
        "productos": [p.model_dump() for p in req.productos],
        "total": req.total
    }

    firma = firmar_factura(SK_EMPRESA, factura)

    return {
        "factura": factura,
        "nit": "900123456",
        "firmaEmpresa": firma
    }

@app.get("/public-key")
def get_public_key():
    return {
        "public_key": PK_EMPRESA.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        ).hex()
    }