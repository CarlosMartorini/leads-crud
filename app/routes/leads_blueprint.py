from flask import Blueprint
from app.controllers.leads_controller import create_lead, delete_lead, get_all_leads, update_lead, delete_lead

bp = Blueprint('leads_bp', __name__, url_prefix='/lead')

bp.post('')(create_lead)
bp.get('')(get_all_leads)
bp.patch('/<string:email>')(update_lead)
bp.delete('/<string:email>')(delete_lead)

