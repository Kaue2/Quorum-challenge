from flask import Blueprint, jsonify
from app.utils.paths import CSV_PATHS
from app.models.data_loader import DataLoader
from app.services.summary_service import SummaryService

legislators_bp = Blueprint("legislators", __name__)

loader = DataLoader()
summary_service = SummaryService()

@legislators_bp.route("/summary", methods=["GET"])
def get_legislators():
    path = CSV_PATHS["legislators"]
    df = summary_service.get_legislators_summary()
    
    if df is None or df.empty: 
        return jsonify({
            "status": "error",
            "message": "No data available. Please upload CSV files first."
            }), 400
        
    return jsonify(df.to_dict(orient="records")), 200