from flask import Blueprint, request, jsonify
from app.database import getDatabase
from app.models.schemas import validarVotante
from bson import ObjectId
from bson.errors import InvalidId
from app.routes.auth import tokenRequired
from app.utils import paginate

voters_bp = Blueprint("voters", __name__)
db = getDatabase()

@voters_bp.route("/voters", methods=["POST"])
@tokenRequired
def createVoter():
    try:
        data = request.get_json()
        valid, err = validarVotante(data)
        if not valid:
            return jsonify({"error": err}), 400
        if db.voters.find_one({"email": data["email"]}) or db.candidates.find_one({"email": data["email"]}):
            return jsonify({"error": "El correo ya está registrado como candidato o votante"}), 400

        data["hasVoted"] = False
        result = db.voters.insert_one(data)
        data["_id"] = str(result.inserted_id)
        return jsonify(data), 201
    except Exception as e:
        return jsonify({"error": f"Error al crear votante: {str(e)}"}), 500
    

@voters_bp.route("/voters", methods=["GET"])
@tokenRequired
def getVoters():
    try:
        page = int(request.args.get("pagina", 1))
        porPagina = int(request.args.get("porPagina", 5))

        cursor = db.voters.find()
        total = db.voters.count_documents({})
        voters = paginate(cursor, page, porPagina)

        votersList = []
        for v in voters:
            v["_id"] = str(v["_id"])
            votersList.append(v)

        return jsonify({"pagina": page, "porPagina": porPagina, "total": total, "votantes": votersList})
    except Exception as e:
        return jsonify({"error": f"Error al obtener la lista de votantes: {str(e)}"}), 500
    

@voters_bp.route("/voters/<id>", methods=["GET"])
@tokenRequired
def getVote(id):
    try:
        voter = db.voters.find_one({"_id": ObjectId(id)})
        if not voter:
            return jsonify({"Error":"No se ha encontrado votante"}), 400
        voter["_id"] = str(voter["_id"])
        return jsonify(voter)
    
    except InvalidId:
        return jsonify({"Error":"ID inválido"}),400

    except Exception as e:
        return jsonify({"Error":f"Error al obtener votante: {str(e)}"}),500
    
@voters_bp.route("/voters/<id>", methods=["DELETE"])
@tokenRequired
def deleteVoter():
    try:
        id = request.view_args.get("id")
        result = db.voters.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            return jsonify({"error": "Votante no encontrado"}), 400
        return jsonify({"atencion": "Votante eliminado correctamente"}), 200
    except InvalidId:
        return jsonify({"error": "ID inválido"}), 400
    except Exception as e:
        return jsonify({"error": f"Error al eliminar al votante: {str(e)}"}), 500