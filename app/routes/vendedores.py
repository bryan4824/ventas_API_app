from fastapi import APIRouter, Query
from uuid import UUID
from app.services.vendedores_services import (get_vendedores, 
                                              list_vendedores, 
                                              create_vendedor, 
                                              update_vendedor, 
                                              delete_vendedor,
                                              get_list_product_by_vendedor)
from app.models.vendedores import (VendedorOut, 
                                   VendedorListOut, 
                                   VendedorCreate, 
                                   VendedorUpdate, 
                                   VendedorListOutByVendedor)

router = APIRouter(prefix="/vendedores", tags=["Vendedores"]) 

# endpoint para listar productos con paginacion
@router.get("/", response_model=VendedorListOut, name = "listar_vendedores")
def list_vendedores_endpoint(
    limit: int = Query(100, ge= 1, le= 100),
    offset: int = Query(0, ge= 0, le = 100)
):
    return list_vendedores(limit = limit, offset= offset)


#endpoint para obtener un  producto por medio de su id
@router.get("/{vendedor_id}", response_model=VendedorOut, description="Obtener_vendedor")
def get_vendedor_endpoint(vendedor_id: UUID):
    return get_vendedores(vendedor_id)

#endpoint para crear un nuevo producto
@router.post("/", response_model= VendedorOut, name="Crear_vendedor")
def crear_vendedor_endpoint(body: VendedorCreate):
    created = create_vendedor(body.model_dump())
    return created

#endpoint para actualizar un producto existente
@router.put("/{vendedor_id}", response_model=VendedorOut, description="Actualizar_vendedor")
def update_vendedor_endpoint(vendedor_id: UUID, body: VendedorUpdate):
    #Con exclude_unset=True (La solución). Esta opción le dice a Pydantic: "Solo dame las llaves que el usuario escribió explícitamente en su JSON".
    updated = update_vendedor(vendedor_id, body.model_dump(exclude_unset=True))
    return updated

#endpoint para eliminar un producto existente
@router.delete("/{vendedor_id}", description="Eliminar_vendedor")
def delete_vendedor_endpoint(vendedor_id: UUID):
    deleted = delete_vendedor(vendedor_id= vendedor_id)
    return deleted

#lista de productos y sus vendedores
# http://localhost:8000/api/v1/productos/vendedor/888f19cb-affb-432d-b7ea-9abdaddb7f47?limit=10&offset=0
@router.get("/{vendedor_id}/productos", response_model=VendedorListOutByVendedor, name = "listar_vendedores_productos")
def list_productos_by_vendedores_endpoint(
    vendedor_id: UUID,
    limit: int = Query(100, ge= 1, le= 100),
    offset: int = Query(0, ge= 0, le = 100)
):
    return get_list_product_by_vendedor(vendedor_id, limit = limit, offset= offset)


