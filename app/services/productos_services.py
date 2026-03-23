from fastapi import HTTPException
from uuid import UUID
from fastapi.encoders import jsonable_encoder
from pydantic import model_validator
from app.models.productos import ProductOut, ProductCreate
from app.core.config import config
from app.core.database import get_supabase

def _table_productos():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_table_productos)

def _table_vendedores():
    sb = get_supabase()
    return sb.schema(config.supabase_schema).table(config.supabase_table_vendedores)

def get_product(product_id: UUID):
    try:
        # Hacemos la consulta a Supabase
        res = _table_productos().select("*").eq("id", str(product_id)).execute()
        
        # 1. Verificamos si la lista de datos está vacía
        if not res.data:
            # Si no hay datos, lanzamos un 404
            raise HTTPException(
                status_code=404, 
                detail=f"El producto con ID {product_id} no fue encontrado"
            )
        
        # 2. Si existe, extraemos el primer (y único) resultado
        data = res.data[0] # recordmeo suq ela pirmera psocion es la 0
        
        # Devolvemos el ítem (aquí podrías usar ProductOut.model_validate(data))
        producto_validado = ProductOut.model_validate(data)
        return producto_validado

    except HTTPException as http_exc:
        # Re-lanzamos el 404 para que no lo capture el Exception genérico
        raise http_exc
        
    except Exception as e:
        # Cualquier otro error (conexión, sintaxis, etc.) devuelve 500
        raise HTTPException(
            status_code=500, 
            detail=f"Error interno al obtener el producto: {str(e)}"
        )

def create_product(datos: dict):
    try:
        # 1. VALIDACIÓN MANUAL: ¿Existe el vendedor?
        # Consultamos la tabla de vendedores usando el ID que viene en los datos
        id_vendedor = datos.get("vendedor_id")
        vendedor_check = _table_vendedores().select("id").eq("id", str(id_vendedor)).execute()
        
        if not vendedor_check.data:
            raise HTTPException(
                status_code=404, 
                detail=f"El vendedor con ID {id_vendedor} no existe. No se puede relacionar el producto."
            )

        # 2. Si existe, procedemos con la inserción
        product_dict = jsonable_encoder(datos) # trasnforma a tipo json datos que model_dump muchas vces no entiende es un seguro de vida extra
        res = _table_productos().insert(product_dict).execute()

        if not res.data:
            raise HTTPException(status_code=400, detail="Error al insertar en la base de datos")
        return ProductOut.model_validate(res.data[0])
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")


def update_product(product_id: UUID, datos:dict):
    try:
        if not datos:
            raise HTTPException(status_code=400, detail="No se recuperaron datos para actualizar")

        body_id = datos.get("id")
        #valida que el id del body y el id de la url sean cosistentes con los datsi que se van a actaulizar
        if body_id and str(product_id) != str(datos.get("id")):
            raise HTTPException (
                status_code=400, 
                detail="Los datos no son cosistentes con el ID a actualizar")
            
        else:
            datos_preparados = jsonable_encoder(datos)
            datos_preparados.pop("id", None)# evitamos actualizatr el producto
            res = _table_productos().update(datos_preparados).eq("id", str(product_id)).execute()
            return ProductOut.model_validate(res.data[0])
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error inesperado al actualizar productos: {str(e)}")        


def delete_product(product_id: UUID):
    try:
        if not product_id:
            raise HTTPException(
                status_code=400, 
                detail="No se recuperaron datos para actualizar")

        res_validator = _table_productos().select("id").eq("id", str(product_id)).execute()
        res_validator = len(res_validator.data)
        if res_validator > 0:
            res = _table_productos().delete().eq("id", str(product_id)).execute()
        else:
            raise HTTPException(
                status_code=404,
                detail=f"El producto con el ID {product_id} no existe"
            )
        return {"details": f"Producto con ID {product_id} eliminado"}
    except HTTPException as he:
        #Si ya es un error HTTP (como el 404), mándalo tal cual
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error inesperado al eliminar productos: {str(e)}")        



def list_products(limit: int = 100, offset: int = 0):
    try:
        # Usamos el string "exact" directamente
        res = _table_productos().select("*", count="exact").range(offset, offset + limit - 1).execute()
        
        # Transformamos los datos a objetos de tu modelo ProductOut
        # Esto es vital para que las fechas y UUIDs se procesen bien
        items_validados = [ProductOut.model_validate(item) for item in res.data]
        
        return {
            "items": items_validados, 
            "total": res.count or 0
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error listando productos: {str(e)}"
        )