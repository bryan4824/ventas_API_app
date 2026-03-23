from app.core.database import get_supabase
import bcrypt
import uuid

def crear_credenciales(vendedor_id: str, username: str, password: str):
    db = get_supabase()
    hashed = bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt()
    ).decode('utf-8')

    result = db.table("credenciales_vendedor").insert({
        "id":          str(uuid.uuid4()),
        "vendedor_id": str(vendedor_id),
        "username":    username,
        "password":    hashed
    }).execute()
    return result.data[0]

def login_vendedor(username: str, password: str):
    db = get_supabase()

    result = db.table("credenciales_vendedor") \
               .select("*, vendedores(*)") \
               .eq("username", username) \
               .execute()

    print("USERNAME BUSCADO:", username)
    print("REGISTROS ENCONTRADOS:", len(result.data))

    if not result.data or len(result.data) == 0:
        raise Exception("Usuario no encontrado")

    credencial = result.data[0]
    print("PASSWORD HASH EN DB:", credencial["password"][:20], "...")

    verificacion = bcrypt.checkpw(
        password.encode('utf-8'),
        credencial["password"].encode('utf-8')
    )
    print("VERIFICACION:", verificacion)

    if not verificacion:
        raise Exception("Contraseña incorrecta")

    return credencial