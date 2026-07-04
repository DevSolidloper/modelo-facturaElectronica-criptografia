from pydantic import BaseModel
from typing import List

class Producto(BaseModel):
    nombre: str
    valor: float

class Factura(BaseModel):
    tokenFiscal: str
    productos: List[Producto]
    total: float

class FacturaRequest(BaseModel):
    factura: Factura
    firmaEmpresa: str
    nit: str







