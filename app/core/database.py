from supabase import create_client, Client
from app.core.config import config


def get_supabase() -> Client:
    try:
        supabase= (create_client(config.SUPABASE_URL, config.SUPABASE_KEY))
        print("Conexion exitisa")
        return supabase
    except Exception as e:
        print(f"Error al crear conexion")
        raise e           
    


     