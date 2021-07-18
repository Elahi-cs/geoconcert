from flask import (
    Blueprint, flash, g, render_template, redirect, request, url_for
)
from werkzeug.exceptions import abort

from geoconcert.auth import login_required

bp = Blueprint('maps', __name__)

@bp.route("/maps/geoconcert")
@login_required
def geoconcert():
    return render_template("maps/geoconcert")