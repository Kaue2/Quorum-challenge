from flask import Blueprint, jsonify

bills_bp = Blueprint("bills", __name__)

@bills_bp.route("/summary", methods=["GET"])
def get_bills():
    return f"rota funcionando"