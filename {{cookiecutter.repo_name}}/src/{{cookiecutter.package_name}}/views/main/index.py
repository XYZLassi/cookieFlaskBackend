from flask_login import login_required
from flask import render_template

from .__bp__ import bp


@bp.route('/', methods=['GET'])
@login_required
def index():
    return render_template('main/index.html')
