from fastapi import HTTPException
from uuid import UUID
from fastapi.encoders import jsonable_encoder
from app.models.vendedores import VendedorOut
from app.models.productos import ProductOut
from app.core.config import config
from app.core.database import get_supabase

def _table_vendedores():
    sb = get_supabase()
    # Asegúrate de que estas variables existan en tu archivo config
    return sb.schema(config.supabase_schema).table(config.supabase_table_vendedores)

def _table_productos():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_table_productos)

# Función para obtener un vendedor por el ID 
def get_vendedores(vendedor_id: UUID): # Cambiado product_id a vendedor_id
    try:
        res = _table_vendedores().select("*").eq("id", str(vendedor_id)).execute()

        if not res.data:
            raise HTTPException(
                status_code=404,
                detail=f"El vendedor con el Id {vendedor_id} no fue encontrado."
            )
        
        return VendedorOut.model_validate(res.data[0])
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error interno al obtener el vendedor: {str(e)}"
        )

# Función para crear un vendedor nuevo
def create_vendedor(data: dict):
    try:
        vendedor_dict = jsonable_encoder(data) 
        res = _table_vendedores().insert(vendedor_dict).execute()

        if not res.data:
            raise HTTPException(status_code=400, detail="Error al insertar el vendedor en la base de datos")

        return VendedorOut.model_validate(res.data[0])
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado al crear vendedor: {str(e)}")

# Función para obtener la lista de vendedores con paginación
def list_vendedores(limit: int = 100, offset: int = 0):
    try:
        res = _table_vendedores().select("*", count="exact").range(offset, offset + limit - 1).execute()
        vendedores_validados = [VendedorOut.model_validate(item) for item in res.data]

        return {
            "items": vendedores_validados,
            "total": res.count or 0
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al listar los vendedores: {str(e)}"
        )
    
# Función para actualizar un vendedor 
def update_vendedor(vendedor_id: UUID, datos: dict):
    try:
        if not datos:
            raise HTTPException(status_code=400, detail="No se enviaron datos para actualizar")

        # Validación de consistencia de ID
        body_id = datos.get("id")
        if body_id and str(vendedor_id) != str(body_id):
            raise HTTPException(
                status_code=400, 
                detail="El ID del cuerpo no coincide con el ID de la URL")
            
        datos_preparados = jsonable_encoder(datos)
        datos_preparados.pop("id", None) # Evitamos intentar actualizar la Primary Key
        
        res = _table_vendedores().update(datos_preparados).eq("id", str(vendedor_id)).execute()
        
        if not res.data:
            raise HTTPException(status_code=404, detail="Vendedor no encontrado para actualizar")

        return VendedorOut.model_validate(res.data[0])
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error inesperado al actualizar vendedor: {str(e)}")        

# Función para eliminar un vendedor
def delete_vendedor(vendedor_id: UUID):
    try:
        # Verificamos existencia antes de borrar
        res_validator = _table_vendedores().select("id").eq("id", str(vendedor_id)).execute()
        
        if not res_validator.data:
            raise HTTPException(
                status_code=404,
                detail=f"El vendedor con el ID {vendedor_id} no existe"
            )

        res = _table_vendedores().delete().eq("id", str(vendedor_id)).execute()
        return {"details": f"Vendedor con ID {vendedor_id} eliminado {res}"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error inesperado al eliminar vendedor: {str(e)}")

def get_list_product_by_vendedor(vendedor_id: UUID, limit = 100, offset: int = 0):
    try:
        if not vendedor_id:
            raise HTTPException(
                status_code=400,
                detail=f"No se recibio ningun ID de busqueda de productos"
            )
        
        #extraemos el nobre pero nos devuelve un paquete con el noombre
        res_name = _table_vendedores().select("nombre").eq("id", str(vendedor_id)).execute()
        #validamos si existe el nombre 
        if not res_name.data:
            raise HTTPException(
                status_code=404,
                detail=f"El vendedor con el ID {vendedor_id} no existe en nuestros registros."
            )
        # si si extraemos solo el nombre del paquete 
        nombre_estraido = res_name.data[0]["nombre"]
        #selecionamos todos los productos por vendedor de ID seleccionaod
        res_products = _table_productos().select("*",count = "exact").eq("vendedor_id", str(vendedor_id)).range(offset, offset+ limit-1). execute()
        
        #retornamos el vendedor y sus productos
        items_validados = [ProductOut.model_validate(item) for item in res_products.data]
        return {
            "nombre_vendedor":nombre_estraido,
            "total": res_products.count or 0,
            "items": items_validados
        }
    except HTTPException as he:
        # ESTO ES CLAVE: Si ya es un error 400 o 404, déjalo pasar tal cual
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error listando productos: {str(e)}"
        )
