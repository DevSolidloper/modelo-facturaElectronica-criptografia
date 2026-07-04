
from fastapi import FastAPI, HTTPException

from app.models.credential import Credential
from app.crypto.verify import verificar_credencial
from app.storage.memory import WALLET_DB
from app.services.registraduria_client import obtener_public_key

from app.services.dian_client import obtener_public_key_dian
from app.crypto.token_fiscal import generar_token_fiscal

app = FastAPI()

@app.post("/store-credential")
def store_credential(payload: Credential):
    data = payload.model_dump()

    firma = data["firma"]
    credencial = {
        "cedula": data["cedula"],
        "nombre": data["nombre"],
        "fecha_nacimiento": data["fecha_nacimiento"]
    }
    
    PK_REG = obtener_public_key()

    valida = verificar_credencial(PK_REG, credencial, firma)

    if not valida:
        raise HTTPException(status_code=400, detail="Credencial invalida")

    WALLET_DB["identity"] = credencial

    return {
        "mensaje" : "Credencial almacenada correctamente"
    }

@app.post("/generate-token")
def generate_token():

    identity = WALLET_DB.get("identity")

    if not identity:
        return {"error": "no identity loaded"}

    pk_dian = obtener_public_key_dian()

    token = generar_token_fiscal(pk_dian, identity["cedula"])

    return {
        "tokenFiscal": token
    }


@app.get("/me")
def me():
    return WALLET_DB.get("identity", {})