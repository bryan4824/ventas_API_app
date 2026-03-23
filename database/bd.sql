-- 1. TABLA DE VENDEDORES
CREATE TABLE vendedores (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  nombre TEXT NOT NULL 
    CHECK (char_length(nombre) >= 8 AND char_length(nombre) <= 60),
  nombre_local TEXT NOT NULL 
    CHECK (char_length(nombre_local) >= 8 AND char_length(nombre_local) <= 60),
  quantity_products INT NOT NULL DEFAULT 0 
    CHECK (quantity_products >= 0),
  direccion TEXT NOT NULL,
  telefono_1 TEXT NOT NULL,
  telefono_2 TEXT, 
  email TEXT NOT NULL UNIQUE 
    CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
  is_activated BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. TABLA DE CATEGORÍAS
CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. TABLA DE PRODUCTOS (Relacionada con Vendedor y Categoría)
CREATE TABLE productos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL CHECK (char_length(name) >= 1),
    price NUMERIC(10, 2) NOT NULL DEFAULT 0 CHECK (price >= 0),
    quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    min_stock INTEGER NOT NULL DEFAULT 0 CHECK (min_stock >= 0),
    ingreso_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- RELACIÓN CON VENDEDOR
    vendedor_id UUID NOT NULL,
    CONSTRAINT fk_vendedor
      FOREIGN KEY(vendedor_id) 
      REFERENCES vendedores(id)
      ON DELETE CASCADE, -- Si el vendedor se elimina, sus productos también

    -- RELACIÓN CON CATEGORÍA
    category_id INTEGER NOT NULL,
    CONSTRAINT fk_categoria
      FOREIGN KEY(category_id) 
      REFERENCES categorias(id)
      ON DELETE RESTRICT -- No permite borrar categoría si tiene productos
);

-- 4. FUNCIÓN Y TRIGGERS PARA UPDATED_AT
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

-- Trigger para Vendedores
CREATE TRIGGER update_vendedores_modtime
    BEFORE UPDATE ON vendedores
    FOR EACH ROW
    EXECUTE PROCEDURE update_modified_column();

-- Trigger para Productos
CREATE TRIGGER update_productos_modtime
    BEFORE UPDATE ON productos
    FOR EACH ROW
    EXECUTE PROCEDURE update_modified_column();