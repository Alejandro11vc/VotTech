from flask import Blueprint, request, jsonify
import jwt
from datetime import datetime, timedelta
from app.config import SECRET_KEY
import os
from dotenv import load_dotenv
load_dotenv()

auth_bp = Blueprint("auth", __name__)

USERNAME = os.getenv("API_USERNAME")
PASSWORD = os.getenv("API_PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        if not data or "username" not in data or "password" not in data:
            return jsonify({"error": "Faltan credenciales"}), 400

        username = data.get("username")
        password = data.get("password")

        if username == USERNAME and password == PASSWORD:
            import time
            token = jwt.encode({
                "user": username,
                "exp": int(time.time()) + 2 * 60 * 60  # 2 horas en segundos
            }, SECRET_KEY, algorithm="HS256")

            return jsonify({"token": token})

        return jsonify({"error": "Credenciales inválidas"}), 401

    except Exception as e:
        return jsonify({"error": f"Error interno: {str(e)}"}), 500
    
def tokenRequired(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            parts = request.headers["Authorization"].split()
            if len(parts) == 2:
                token = parts[1]
        if not token:
            return jsonify({"error": "El token es requerido"}), 401
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except Exception:
            return jsonify({"error": "Token no válido o ha expirado"}), 401
        return f(*args, **kwargs)
    return decorated