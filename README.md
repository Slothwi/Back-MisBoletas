# BackEnd App MisBoletas

## ¡Tener Instalado Python3!

1. Crear entorno virtual e Instalar fastAPI + uvicorn(Servidor)

   ```bash
      python -m venv venv
      .\venv\Scripts\Activate.ps1
   ```

   ```bash
      pip install fastapi uvicorn[standard]
   ```

2. instalar dependencias

   ```bash
   pip install -r requirements.txt
   ```

3. Levantar servidor (uvicorn)

   ```bash
   uvicorn main:app --reload
   ```

4. Crear archivo .env en la raíz del proyecto:

```env
SQLSERVER_SERVER=localhost
SQLSERVER_DATABASE=MisBoletas
SQLSERVER_USERNAME=
SQLSERVER_PASSWORD=
```

5. Verificar conexión a BD

   ```bash
      python test_existing_db.py
   ```

## 🌐 URLs disponibles

- **API:** http://127.0.0.1:8000
- **Documentación:** http://127.0.0.1:8000/docs
- **Usuarios:** http://127.0.0.1:8000/api/v1/users

