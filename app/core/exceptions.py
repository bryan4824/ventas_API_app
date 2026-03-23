from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

# Diccionario unificado para Productos y Vendedores
DICCIONARIO_ERRORES_API = {
    # --- PRODUCTOS ---
    "listar_productos": {
        "limit": {
            "greater_than_equal": "El límite debe ser al menos 1",
            "less_than_equal": "El límite máximo permitido es 500",
            "int_parsing": "El límite debe ser un número entero válido"
        },
        "offset": {
            "greater_than_equal": "El offset no puede ser negativo",
            "int_parsing": "El offset debe ser un número entero válido"
        }
    },
    "get_product": {
        "product_id": {
            "uuid_parsing": "El ID del producto debe ser un UUID válido",
            "missing": "El ID del producto es obligatorio"
        }
    },
    "Create_product": {
        "body": {
            "missing": "Se requiere la información del producto para crearlo",
            "invalid_schema": "Los datos del producto no cumplen con el formato requerido"
        }
    },

    # --- VENDEDORES ---
    "listar_vendedores": {
        "limit": {
            "greater_than_equal": "El límite debe ser al menos 1",
            "less_than_equal": "El límite máximo para vendedores es 100",
            "int_parsing": "El límite debe ser un número entero"
        },
        "offset": {
            "greater_than_equal": "El offset no puede ser negativo",
            "int_parsing": "El offset debe ser un número entero"
        }
    },
    "Crear_vendedor": {
        "body": {
            "missing": "Se requiere el cuerpo con los datos del vendedor",
            "invalid_schema": "La estructura del vendedor es incorrecta"
        }
    },
    "listar_vendedores_productos": {
        "vendedor_id": {
            "uuid_parsing": "El ID del vendedor debe ser un UUID válido"
        },
        "limit": {"greater_than_equal": "El límite debe ser al menos 1"},
        "offset": {"greater_than_equal": "El offset no puede ser negativo"}
    }
}

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errores_personalizados = []
    
    # Obtenemos la ruta que falló
    route_obj = request.scope.get("route")
    nombre_ruta = getattr(route_obj, "name", None)
    
    for err in exc.errors():
        # 'loc' suele ser ('query', 'limit') o ('body', 'nombre')
        campo = str(err["loc"][-1])
        tipo_error = err["type"]
        
        # Intentamos buscar el mensaje en nuestro diccionario
        mensaje = (
            DICCIONARIO_ERRORES_API.get(nombre_ruta, {})
            .get(campo, {})
            .get(tipo_error)
        )
        
        # Si no existe en el diccionario, usamos el mensaje por defecto de FastAPI
        if not mensaje:
            mensaje = f"Error en el campo '{campo}': {err['msg']}"
            
        errores_personalizados.append(mensaje)

    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "tipo": "Validación de datos",
            "detalles": errores_personalizados
        }
    )