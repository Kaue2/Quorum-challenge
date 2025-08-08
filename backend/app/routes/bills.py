from flask import Blueprint, jsonify
from app.models.data_loader import DataLoader
from app.services.summary_service import SummaryService

bills_bp = Blueprint("bills", __name__)

loader = DataLoader()
service = SummaryService(loader)

@bills_bp.route("/summary", methods=["GET"])
def get_bills():
    df = service.get_bill_summary()
    return jsonify(df.to_dict(orient="records"))