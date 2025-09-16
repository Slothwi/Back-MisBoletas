"""
Test simple para verificar conexión a base de datos existente
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import engine, SessionLocal
from app.models import Usuario

def test_existing_database():
    """Prueba conectar a la base de datos existente"""
    print("Conectando a base de datos existente...")
    
    # Test de conexión
    connection = engine.connect()
    if connection:
        print("Conexión exitosa!")
        connection.close()
    else:
        print("Error de conexión")
        return False
    
    # Test de consulta a tabla existente
    print("Consultando tabla Usuarios existente...")
    db = SessionLocal()
    
    try:
        # Contar usuarios existentes
        count = db.query(Usuario).count()
        print(f"Se encontraron {count} usuarios en la tabla")
        
        # Mostrar algunos usuarios si existen
        if count > 0:
            usuarios = db.query(Usuario).limit(5).all()
            print("Usuarios encontrados:")
            for user in usuarios:
                print(f" - ID: {user.UsuarioID}, Nombre: {user.NombreUsuario}, Email: {user.Email}")
        else:
            print("La tabla está vacía, pero la conexión funciona")
            
    except Exception as e:
        print(f"Error consultando la tabla: {e}")
        return False
    finally:
        db.close()
    
    print("¡Conexión a base de datos existente verificada!")
    return True

if __name__ == "__main__":
    test_existing_database()