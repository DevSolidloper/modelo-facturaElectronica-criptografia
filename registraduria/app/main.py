from fastapi import FastAPI

from app.crypto.keys import cargar_o_generar_claves
from app.models.credential import Credential
from app.crypto.signing import firmar_credencial
import json
from cryptography.hazmat.primitives import serialization

app = FastAPI()

SK_REG, PK_REG = cargar_o_generar_claves()

@app.get("/")
def home():
    return {
        "mensaje": "Servicio Registraduria funcionando"
    }

@app.post("/emitir_credencial")
def emitir_credencial(credential: Credential):
    credential_dict = credential.model_dump()

    firma = firmar_credencial(SK_REG, credential_dict)

    return{
        "credencial" : credential_dict,
        "firma" : firma 
    }

@app.get("/public-key")
def get_public_key():
    return {
        "public_key": PK_REG.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        ).hex()
    }

