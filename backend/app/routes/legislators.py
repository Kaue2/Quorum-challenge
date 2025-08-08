from flask import Blueprint, jsonify
from app.utils.paths import CSV_PATHS
from app.models.data_loader import DataLoader
from app.services.summary_service import SummaryService

legislators_bp = Blueprint("legislators", __name__)

loader = DataLoader()
service = SummaryService(loader)

@legislators_bp.route("/summary", methods=["GET"])
def get_legislators():
    path = CSV_PATHS["legislators"]
    df = service.get_legislators_summary()
    return jsonify(df.to_dict(orient="records"))