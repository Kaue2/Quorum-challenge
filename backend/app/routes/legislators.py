from flask import Blueprint, jsonify

legislators_bp = Blueprint("legislators", __name__)

@legislators_bp.route("/summary", methods=["GET"])
def get_legislators():
    return f"rota funcionando"