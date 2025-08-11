from flask import Blueprint, jsonify
from app.utils.paths import CSV_PATHS
from app.models.data_loader import DataLoader
from app.services.summary_service import SummaryService

# Blueprint for legislators-related endpoints
legislators_bp = Blueprint("legislators", __name__)

# Initialize singleton instances
loader = DataLoader()
summary_service = SummaryService()

@legislators_bp.route("/summary", methods=["GET"])
def get_legislators():
    """
    Endpoint to get summary of legislators with their voting records
    Returns: JSON with legislator information including supported and opposed bills count
    """
    # Get legislators summary data from service
    df = summary_service.get_legislators_summary()
    
      # Check if data is available
    if df is None or df.empty: 
        return jsonify({
            "status": "error",
            "message": "No data available. Please upload CSV files first."
            }), 400
        
    # Return data as JSON records
    return jsonify(df.to_dict(orient="records")), 200