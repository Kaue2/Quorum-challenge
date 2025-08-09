from flask import Blueprint, jsonify
from app.models.data_loader import DataLoader
from app.services.summary_service import SummaryService

bills_bp = Blueprint("bills", __name__)

loader = DataLoader()
summary_service = SummaryService()

@bills_bp.route("/summary", methods=["GET"])
def get_bills():
    df = summary_service.get_bill_summary()
    
    if df is None or df.empty: 
        return jsonify({
            "status": "error",
            "message": "No data available. Please upload CSV files first."
            }), 400
    
    return jsonify(df.to_dict(orient="records")),200