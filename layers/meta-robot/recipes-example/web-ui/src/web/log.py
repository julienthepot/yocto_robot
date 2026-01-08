import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from web.db import get_db

bp = Blueprint('log', __name__, url_prefix='/log')


@bp.route('/logs')
def logs():
    db = get_db()
    logs = db.execute(
        'SELECT id, created, level, message FROM log ORDER BY created DESC'
    ).fetchall()
    return render_template('log/logs.html', logs=logs)