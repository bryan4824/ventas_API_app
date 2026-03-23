from fastapi import APIRouter, HTTPException
from app.models.vendedores import CredencialesCreate, LoginVendedor
from app.services.credenciales_services import crear_credenciales, login_vendedor
from app.core.database import get_supabase
import bcrypt

router = APIRouter(prefix="/credenciales", tags=["Credenciales"])

@router.post("/", summary="Crear credenciales de vendedor")
def crear(body: CredencialesCreate):
    try:
        result = crear_credenciales(
            str(body.vendedor_id),
            body.username,
            body.password
        )
        return result
    except Exception as e:
        print("ERROR DETALLADO:", str(e))  
        import traceback
        traceback.print_exc()              
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login", summary="Login de vendedor")
def login(body: LoginVendedor):
    try:
        credencial = login_vendedor(body.username, body.password)
        return { "success": True, "data": credencial }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/", summary="Listar todas las credenciales")
def listar():
    db = get_supabase()
    result = db.table("credenciales_vendedor").select("*, vendedores(*)").execute()
    return result.data

@router.put("/{cred_id}", summary="Actualizar credenciales")
def actualizar(cred_id: str, body: dict):
    db = get_supabase()
    update = { "username": body.get("username") }
    if body.get("password"):
        update["password"] = bcrypt.hashpw(body["password"].encode(), bcrypt.gensalt()).decode()
    db.table("credenciales_vendedor").update(update).eq("id", cred_id).execute()
    return { "success": True }

@router.delete("/{cred_id}", summary="Eliminar credenciales")
def eliminar(cred_id: str):
    db = get_supabase()
    db.table("credenciales_vendedor").delete().eq("id", cred_id).execute()
    return { "success": True }