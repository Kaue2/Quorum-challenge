from flask import Blueprint, request, jsonify
import os
from app.models.data_loader import DataLoader
from app.services.summary_service import SummaryService
from app.utils.paths import CSV_PATHS

upload_bp = Blueprint("upload", __name__)

loader = DataLoader()
summary_service = SummaryService()

@upload_bp.route("/upload-csvs", methods=["POST"])
def upload_csvs(): 
    required_files = {
        'legislators': 'legislators.csv',
        'bills': 'bills.csv',
        'votes': 'votes.csv',
        'vote_results': 'vote_results.csv'
    }
    
    upload_folder = os.path.join(os.getcwd(), "uploads")
    os.makedirs(upload_folder, exist_ok=True)
    
    for key, filename in required_files.items(): 
        file = request.files.get(key)
        if not file: 
            return jsonify({"error": f"File {filename} was not receivid"}), 400
        save_path = os.path.join(upload_folder, filename)
        file.save(save_path)
        
        CSV_PATHS[key] = save_path
        
    loader.load_files()
    summary_service.refresh_data()
    
    return jsonify({"Message": "All files received and uploaded"}), 200