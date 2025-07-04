# VotTech API

API REST para gestión de votaciones desarrollada en **Python + Flask + MongoDB**

## Tecnologías

- Python 3.10+
- Flask
- Flask-JWT-Extended
- PyMongo
- MongoDB Atlas
- Dotenv
- Postman (para pruebas)

## Requisitos

- Python 3.10+
- MongoDB Atlas o local

## Instalación

```bash
1. Clona este repositorio:
```bash
git clone https://github.com/TU_USUARIO/Vottech.git

cd votaciones-api

2. Crea y activa un entorno virtual:
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

3. Instala todas las dependencias necesarias:
pip install -r requirements.txt
#Esto instalará automáticamente Flask, flask-cors, PyJWT, pymongo, python-dotenv y todas las librerías necesarias para que el proyecto funcione correctamente.

4. Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido y tus propios valores. Por ejemplo:

5. Ejecuta la API:
python main.py
```

```
Configuración de la base de datos y credenciales para login:

MONGO_URI=mongodb://localhost:27017
MONGO_DB=voting_db
API_USERNAME=admin
API_PASSWORD=admin123
SECRET_KEY=alguna_clave_secreta
```

- El usuario y contraseña (`API_USERNAME` y `API_PASSWORD`) serán los que usarás para hacer login en la API.
- Puedes poner cualquier valor que desees para tus pruebas locales.
- Si usas MongoDB Compass/local, la URI típica es: `mongodb://localhost:27017`
- Si usas MongoDB Atlas, obtén la URI desde el panel de Atlas.

Autenticación:
Endpoint: POST /login
{
  "username": "admin",
  "password": "admin123"
}
Obtendrás un token JWT. Usa este token en los siguientes endpoints como Bearer Token.

## Endpoints principales

- POST `/login` — Obtener token JWT
- POST `/voters` — Crear votante (requiere token)
- GET `/voters` — Listar votantes (requiere token)
- GET `/voters/<id>` — Obtener votante por id (requiere token)
- POST `/candidates` — Crear candidato (requiere token)
- GET `/candidates` — Listar candidatos (requiere token)
- GET `/candidates/<id>` — Obtener candidato por id (requiere token)
- POST `/votes` — Registrar voto (requiere token)
- GET `/votes` — Listar votos (requiere token)
- GET `/votes/statistics` — Ver estadísticas (requiere token)


```markdown
---

## 📸 Capturas del sistema

📷 Estadísticas generadas:

![Estadísticas](capturas/estadisticas.png)

![Login](capturas/login.png)