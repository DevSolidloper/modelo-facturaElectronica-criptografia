from pydantic import BaseModel
from typing import List

class Producto(BaseModel):
    nombre: str
    valor: float


class FacturaRequest(BaseModel):
    tokenFiscal: str
    productos: List[Producto]
    total: float