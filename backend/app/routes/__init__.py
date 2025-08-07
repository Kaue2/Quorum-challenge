from .legislators import legislators_bp
from .bills import bills_bp

def register_routes(app):
    app.register_blueprint(legislators_bp, url_prefix="/api/legislators")
    app.register_blueprint(bills_bp, url_prefix="/api/bills")