from flask import Blueprint, request, jsonify
from app.database import getDatabase
from bson import ObjectId
from bson.errors import InvalidId
from app.models.schemas import validarVoto
from app.routes.auth import tokenRequired

votes_bp = Blueprint("votes", __name__)
db = getDatabase()

@votes_bp.route("/votes", methods=["POST"])
@tokenRequired
def castVote():
    try:
        data = request.get_json()
        valid, err = validarVoto(data)
        if not valid:
            return jsonify({"error": err}), 400

        try:
            voterId = ObjectId(data["voterId"])
            candidateId = ObjectId(data["candidateId"])

        except InvalidId:
            return jsonify({"error": "ID de votante o candidato inválido"}), 400

        voter = db.voters.find_one({"_id": voterId})
        candidate = db.candidates.find_one({"_id": candidateId})

        if not voter:
            return jsonify({"error": "El votante no ha sido encontrado"}), 400
        if voter.get("hasVoted"):
            return jsonify({"error": "Ya ha votado. Solo se permite un voto por persona"}), 400
        if not candidate:
            return jsonify({"error": "Candidato no válido"}), 400

        vote = {"voterId": voterId, "candidateId": candidateId}
        db.votes.insert_one(vote)

        db.voters.update_one({"_id": voterId}, {"$set": {"hasVoted": True}})
        db.candidates.update_one({"_id": candidateId}, {"$inc": {"votes": 1}})

        return jsonify({"message": "El voto se ha registrado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": f"Error al realizar el voto: {str(e)}"}), 500
    
@votes_bp.route("/votes", methods=["GET"])
@tokenRequired
def getVotes():
    try:
        votes = []
        for v in db.votes.find():
            votes.append({
                "_id": str(v["_id"]),
                "voterId": str(v["voterId"]),
                "candidateId": str(v["candidateId"])
            })
        return jsonify(votes)

    except Exception as e:
        return jsonify({"error": f"Error interno al obtener votos: {str(e)}"}), 500

@votes_bp.route("/votes/statistics", methods=["GET"])
@tokenRequired
def voteStatistics():
    try:
        totalVotes = db.votes.count_documents({})

        # Obtener votos por candidato
        pipeline = [
            {
                "$group": {
                    "_id": "$candidateId",
                    "votesCount": {"$sum": 1}
                }
            }
        ]
        votesCandidate = list(db.votes.aggregate(pipeline))

        results = []
        for item in votesCandidate:
            candidate = db.candidates.find_one({"_id": item["_id"]})
            if candidate:
                porcentage = (item["votesCount"] / totalVotes * 100) if totalVotes > 0 else 0
                results.append({
                    "candidate": candidate["name"],
                    "votes": item["votesCount"],
                    "percentage": round(porcentage, 2)
                })

        # Contar votantes que han votado
        votersVoted = db.voters.count_documents({"hasVoted": True})

        return jsonify({"totalVotes": totalVotes,"votersVoted": votersVoted,"results": results
        })

    except Exception as e:
        return jsonify({"error": f"Error interno al obtener estadísticas: {str(e)}"}), 500