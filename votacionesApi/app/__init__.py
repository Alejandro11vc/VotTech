from flask import Flask
from app.routes.voters import voters_bp
from app.routes.candidates import candidates_bp
from app.routes.votes import votes_bp
from app.routes.auth import auth_bp

def create_app():
    app = Flask(__name__)

    # Rutas registradas
    app.register_blueprint(voters_bp)
    app.register_blueprint(candidates_bp)
    app.register_blueprint(votes_bp)
    app.register_blueprint(auth_bp)

    return app
