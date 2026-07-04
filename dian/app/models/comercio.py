from pydantic import BaseModel

class ComercioRegistro(BaseModel):
    nit: str
    public_key: str