from flask import Flask
from flask_cors import CORS
from app.routes.voters import voters_bp
from app.routes.candidates import candidates_bp
from app.routes.votes import votes_bp
from app.routes.auth import auth_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(voters_bp)
app.register_blueprint(candidates_bp)
app.register_blueprint(votes_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)
