from pydantic import BaseModel

class Credential(BaseModel):
    cedula: str
    nombre: str
    fecha_nacimiento: str
    firma: str