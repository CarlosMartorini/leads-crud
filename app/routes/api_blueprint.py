from flask import Blueprint
from . import leads_blueprint

bp = Blueprint('api_bp', __name__, url_prefix='/api')

bp.register_blueprint(leads_blueprint.bp)