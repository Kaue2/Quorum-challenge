from flask import Blueprint, jsonify
from app.models.data_loader import DataLoader
from app.services.summary_service import SummaryService

# Blueprint for bills-related endpoints
bills_bp = Blueprint("bills", __name__)

# Initialize singleton instances
loader = DataLoader()
summary_service = SummaryService()

@bills_bp.route("/summary", methods=["GET"])
def get_bills():
    """
    Endpoint to get summary of bills with support/opposition counts
    Returns: JSON with bill information including supporters, opposers, and primary sponsor
    """
    # Get bill summary data from service
    df = summary_service.get_bill_summary()
    
    # Check if data is available
    if df is None or df.empty: 
        return jsonify({
            "status": "error",
            "message": "No data available. Please upload CSV files first."
            }), 400
    
    # Return data as JSON records
    return jsonify(df.to_dict(orient="records")),200