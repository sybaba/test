from flask import Blueprint, render_template
from app.models import instances

instance_bp = Blueprint('instance_bp', __name__, url_prefix='/instances')

@instance_bp.route('/')
def list_instances():
    return render_template('instances.html', instances=instances)