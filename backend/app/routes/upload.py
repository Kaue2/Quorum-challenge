from flask import Blueprint, request, jsonify
import os
from app.models.data_loader import DataLoader
from app.services.summary_service import SummaryService
from app.utils.paths import CSV_PATHS

# Blueprint for handling file uploads
upload_bp = Blueprint("upload", __name__)

# Initialize singleton instances
loader = DataLoader()
summary_service = SummaryService()

@upload_bp.route("/upload-csvs", methods=["POST"])
def upload_csvs(): 
    """
    Endpoint to upload CSV files for legislative data
    Expects 4 files: legislators, bills, votes, vote_results
    """
    # Dictionary mapping form field names to expected filenames
    required_files = {
        'legislators': 'legislators.csv',
        'bills': 'bills.csv',
        'votes': 'votes.csv',
        'vote_results': 'vote_results.csv'
    }
    
    # Create uploads directory if it doesn't exist
    upload_folder = os.path.join(os.getcwd(), "uploads")
    os.makedirs(upload_folder, exist_ok=True)
    
    # Process each required file
    for key, filename in required_files.items(): 
        # Check if file was provided in the request
        file = request.files.get(key)
        if not file: 
            return jsonify({"error": f"File {filename} was not receivid"}), 400
        
        # Save file to uploads directory
        save_path = os.path.join(upload_folder, filename)
        file.save(save_path)
        
         # Update the CSV_PATHS dictionary with new file location
        CSV_PATHS[key] = save_path
        
    # Load the new files into the application
    loader.load_files()
    
    # Refresh data in summary service
    summary_service.refresh_data()
    
    return jsonify({"Message": "All files received and uploaded"}), 200