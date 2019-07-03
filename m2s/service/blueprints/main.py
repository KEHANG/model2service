from flask import Blueprint, current_app, Response

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    return Response(response=current_app.title, status=200)