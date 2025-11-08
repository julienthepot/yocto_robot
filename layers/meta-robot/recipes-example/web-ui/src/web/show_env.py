import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from web.db import get_db

bp = Blueprint('show_env', __name__, url_prefix='/')


@bp.route('/show_env')
def show_env():
    return render_template('show_env.html')