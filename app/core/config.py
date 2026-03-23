from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    # Asegúrate de que cada alias coincida con el nombre exacto en tu .env
    SUPABASE_URL: str = Field(default="", alias="SUPABASE_URL")
    SUPABASE_KEY: str = Field(default="", alias="SUPABASE_KEY")
    supabase_schema: str = Field(default="public", alias="SUPABASE_SCHEMA") # Corregido el alias
    supabase_table_productos: str = Field(default="productos", alias="SUPABASE_TABLE_PRODUCTOS")
    supabase_table_vendedores: str = Field(default="vendedores", alias="SUPABASE_TABLE_VENDEDORES")
    supabase_table_credenciales: str = Field(default="credenciales_vendedor", alias="SUPABASE_TABLE_CREDENCIASLES_VENDEDORES")

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )

config = Config()