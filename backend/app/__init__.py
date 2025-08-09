from flask import Flask
from flask_cors import CORS
from app.routes import register_routes
from app.models.data_loader import DataLoader
from app.services.summary_service import SummaryService

def create_app():
    app = Flask(__name__)
    CORS(app)
    register_routes(app)
    data_loader = DataLoader()
    summary_service = SummaryService(data_loader)
    return app