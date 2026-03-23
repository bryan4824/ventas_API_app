from fastapi import APIRouter, Query, status
from uuid import UUID
from app.services.productos_services import get_product, list_products, create_product, update_product, delete_product
from app.models.productos import ProductOut, ProductListOut, ProductCreate, ProductUpdate

router = APIRouter(prefix="/productos", tags=["Productos"]) 

# endpoint para listar productos con paginacion
@router.get(
    "/", 
    response_model=ProductListOut, 
    name="listar_productos",
    summary="Listar Productos",
    description="Retorna una lista paginada de productos."
)
def home(
    limit: int = Query(100, ge=1, le=500, description="Límite de registros"),
    offset: int = Query(0, ge=0, description="Inicio de la paginación")
):
    return list_products(limit, offset)

#endpoint para obtener un producto por medio de su id
@router.get(
    "/{product_id}", 
    response_model=ProductOut, 
    name="get_product",
    summary="Obtener Producto",
    description="Busca un producto por su UUID único."
)
def get_product_endpoint(product_id: UUID):
    # Simplemente retorna el resultado de la función
    return get_product(product_id)

#endpoint para crear un nuevo producto
@router.post(
    "/", 
    response_model=ProductOut, 
    name="Create_product", 
    status_code=status.HTTP_201_CREATED,
    summary="Crear Producto",
    description="Crea un nuevo producto en la base de datos."
)
def create_product_endpoint(body: ProductCreate):
    # fast api valida que en el body los datos que se envian tengas consistemcia con el modelo
    created = create_product(body.model_dump())
    return created

#endpoint para actualizar un producto existente
@router.put(
    "/{producto_id}", 
    response_model=ProductOut, 
    description="Actualizar_producto",
    summary="Actualizar Producto"
)
def update_product_endpoint(producto_id: UUID, body: ProductUpdate):
    #Con exclude_unset=True (La solución). Esta opción le dice a Pydantic: "Solo dame las llaves que el usuario escribió explícitamente en su JSON".
    updated = update_product(producto_id, body.model_dump(exclude_unset=True))
    return updated
    
#endpoint para eliminar un producto existente
@router.delete(
    "/{product_id}", 
    description="Eliminar_product",
    summary="Eliminar Producto",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_product_endpoint(product_id: UUID):
    deleted = delete_product(product_id=product_id)
    return deleted