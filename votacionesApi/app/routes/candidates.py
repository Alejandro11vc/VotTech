from flask import Blueprint, request, jsonify
from app.database import getDatabase
from app.models.schemas import validarCandidato
from bson import ObjectId
from bson.errors import InvalidId
from app.routes.auth import tokenRequired
from app.utils import paginate

candidates_bp = Blueprint("candidates", __name__)
db = getDatabase()

@candidates_bp.route("/candidates", methods=["POST"])
@tokenRequired
def createCandidate():
    try:
        data = request.get_json()
        valid, err = validarCandidato(data)

        if not valid:
            return jsonify({"error": err}), 400

        if db.candidates.find_one({"email": data.get("email")}) or db.voters.find_one({"email": data.get("email")}):
            return jsonify({"error": "El correo ya está registrado como candidato o votante"}), 400

        data["votes"] = 0
        result = db.candidates.insert_one(data)
        data["_id"] = str(result.inserted_id)
        return jsonify(data), 201
    except Exception as e:
        return jsonify({"error": f"Error al crear candidato: {str(e)}"}), 500
    
@candidates_bp.route("/candidates", methods=["GET"])
@tokenRequired
def getCandidates():
    try:
        pagina = int(request.args.get("pagina", 1))
        porPagina = int(request.args.get("porPagina", 5))

        cursor = db.candidates.find()
        total = db.candidates.count_documents({})
        candidates = paginate(cursor, pagina, porPagina)

        candidatesList = []
        for c in candidates:
            c["_id"] = str(c["_id"])
            candidatesList.append(c)

        return jsonify({"pagina": pagina, "porPagina": porPagina, "total": total, "candidatos": candidatesList})
    except Exception as e:
        return jsonify({"error": f"Error al obtener los candidatos: {str(e)}"}), 500

@candidates_bp.route("/candidates/<id>", methods=["GET"])
@tokenRequired
def getCandidate(id):
    try:
        candidate = db.candidates.find_one({"_id": ObjectId(id)})
        if not candidate:
            return jsonify({"error": "Candidato no encontrado"}), 404
        candidate["_id"] = str(candidate["_id"])
        return jsonify(candidate)
    except InvalidId:
        return jsonify({"error": "ID inválido"}), 400
    except Exception as e:
        return jsonify({"error": f"Error al obtener el candidato: {str(e)}"}), 500
    

@candidates_bp.route("/candidates/<id>", methods=["DELETE"])
@tokenRequired
def delteCandidate(id):
    try:
        result = db.candidates.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            return jsonify({"error": "Candidato no encontrado"}), 404
        return jsonify({"mensaje": "Candidato eliminado correctamente"}), 200
    except InvalidId:
        return jsonify({"error": "ID inválido"}), 400
    except Exception as e:
        return jsonify({"error": f"Error al eliminar candidato: {str(e)}"}), 500
