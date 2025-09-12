"""
Test simple para insertar usuario en base de datos existente
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models import Usuario

def insert_test_user():
    """Insertar un usuario de prueba en la base de datos"""
    print("Conectando a la base de datos...")
    
    db = SessionLocal()
    
    # Datos del usuario a insertar
    test_user = Usuario(
        NombreUsuario="UsuarioPrueba",
        Email="test@misBoletas.com",
        ContraseñaHash="hash_password_123"
    )
    
    # Verificar si ya existe
    existing = db.query(Usuario).filter(Usuario.Email == test_user.Email).first()
    if existing:
        print(f"Usuario ya existe: {existing.NombreUsuario} (ID: {existing.UsuarioID})")
        db.close()
        return existing
    
    # Insertar nuevo usuario
    print("Insertando nuevo usuario...")
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    
    if test_user.UsuarioID:
        print(f"Usuario insertado exitosamente!")
        print(f"   - ID: {test_user.UsuarioID}")
        print(f"   - Nombre: {test_user.NombreUsuario}")
        print(f"   - Email: {test_user.Email}")
    else:
        print("Error al insertar usuario")
    
    db.close()
    return test_user

def view_all_users():
    """Ver todos los usuarios en la base de datos"""
    print("\n Consultando todos los usuarios...")
    
    db = SessionLocal()
    usuarios = db.query(Usuario).all()
    
    if usuarios:
        print(f"Se encontraron {len(usuarios)} usuarios:")
        for user in usuarios:
            print(f"   - ID: {user.UsuarioID} | {user.NombreUsuario} | {user.Email}")
    else:
        print("No hay usuarios en la base de datos")

    db.close()
    return usuarios

if __name__ == "__main__":
    print("=== TEST DE INSERCIÓN DE USUARIO ===\n")
    
    # Insertar usuario de prueba
    user = insert_test_user()
    
    # Ver todos los usuarios
    view_all_users()

    print("\n Test completado!")