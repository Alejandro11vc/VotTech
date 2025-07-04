def validarVotante(data):
    if not data.get("name") or not data.get("email"):
        return False, "El nombre y el correo electrónico son obligatorios."
    return True, ""

def validarCandidato(data):
    if not data.get("name"):
        return False, "El nombre del candidato es obligatorio."
    return True, ""

def validarVoto(data):
    if not data.get("voterId") or not data.get("candidateId"):
        return False, "Los campos voterId y candidateId son requeridos."
    return True, ""
