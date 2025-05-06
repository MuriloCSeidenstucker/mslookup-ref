from flask import Flask

from mslookup_ref.main.routes.routes import medicine_route_bp

app = Flask(__name__)

app.register_blueprint(medicine_route_bp)
