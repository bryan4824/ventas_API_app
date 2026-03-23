from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime, date
from typing import Optional, List

class ProductCreate(BaseModel):
    vendedor_id: UUID
    name: str = Field(..., min_length=1, max_length=200)
    descripcion: Optional[str] = None
    precio: float = Field(default=0.0, ge=0)          # ✅ precio no price
    descuento: Optional[float] = Field(default=0.0, ge=0)
    servicio_a_domicilio: Optional[bool] = False
    tipo_de_pago: Optional[str] = None
    quantity: int = Field(default=0, ge=0)
    min_stock: int = Field(default=0, ge=0)
    max_stock: Optional[int] = Field(default=0, ge=0)
    ubicacion_exacta: Optional[str] = None
    ingreso_date: Optional[date] = None
    category_id: Optional[int] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    descripcion: Optional[str] = None
    precio: Optional[float] = Field(None, ge=0)       # ✅ precio no price
    descuento: Optional[float] = Field(None, ge=0)
    servicio_a_domicilio: Optional[bool] = None
    tipo_de_pago: Optional[str] = None
    quantity: Optional[int] = Field(None, ge=0)
    min_stock: Optional[int] = Field(None, ge=0)
    max_stock: Optional[int] = Field(None, ge=0)
    ubicacion_exacta: Optional[str] = None
    ingreso_date: Optional[date] = None
    category_id: Optional[int] = None

class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    vendedor_id: UUID
    name: str
    descripcion: Optional[str] = None
    precio: Optional[float] = Field(default=0.0, ge=0)  # ✅
    descuento: Optional[float] = None
    servicio_a_domicilio: Optional[bool] = None
    tipo_de_pago: Optional[str] = None
    quantity: int = Field(default=0, ge=0)
    min_stock: int = Field(default=0, ge=0)
    max_stock: Optional[int] = None
    ubicacion_exacta: Optional[str] = None
    ingreso_date: Optional[date] = None
    category_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class ProductListOut(BaseModel):
    total: int
    items: List[ProductOut]