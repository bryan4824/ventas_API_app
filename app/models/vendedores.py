from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime, date  # <-- Corregido
from typing import Optional, List
from app.models.productos import ProductOut
from pydantic import BaseModel


class VendedorBase(BaseModel):
    nombre: str = Field(..., min_length=8, max_length=60)
    nombre_local: str = Field(..., min_length=8, max_length=60)
    direccion: str = Field(...)
    telefono_1: str = Field(...)
    telefono_2: Optional[str] = None
    email: str = Field(..., pattern=r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
    is_activated: bool = True

class VendedorCreate(VendedorBase):
    # Hereda todo lo de Base y solo agregamos quantity_products
    # Usamos True de Python, no true de sqlmodel
    is_activated: bool = Field(default=True) 
    
class VendedorUpdate(BaseModel):
    # Todo opcional para PATCH
    nombre: Optional[str] = Field(None, min_length=8, max_length=60)
    nombre_local: Optional[str] = Field(None, min_length=8, max_length=60)
    direccion: Optional[str] = None
    telefono_1: Optional[str] = None
    telefono_2: Optional[str] = None
    email: Optional[str] = Field(None, pattern=r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
    is_activated: Optional[bool] = None

class VendedorOut(VendedorBase):
    id: UUID
    quantity_products: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class VendedorListOut(BaseModel):
    #Salisa de numero total de registros 
    total: int
    items: List[VendedorOut]


class VendedorListOutByVendedor(BaseModel):
    #Salisa de numero total de registros 
    nombre_vendedor: str
    total: int
    items: List[ProductOut]

#modelos de credenciales

class CredencialesCreate(BaseModel):
    vendedor_id: UUID
    username: str
    password: str

class CredencialesOut(BaseModel):
    id: UUID
    vendedor_id: UUID
    username: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class LoginVendedor(BaseModel):
    username: str
    password: str