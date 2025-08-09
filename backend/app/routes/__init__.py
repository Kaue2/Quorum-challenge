from .legislators import legislators_bp
from .bills import bills_bp
from .upload import upload_bp

def register_routes(app):
    app.register_blueprint(legislators_bp, url_prefix="/api/legislators")
    app.register_blueprint(bills_bp, url_prefix="/api/bills")
    app.register_blueprint(upload_bp, url_prefix="/api")