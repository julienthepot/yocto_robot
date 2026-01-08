import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from web.db import get_db

bp = Blueprint('ui', __name__, url_prefix='/')


@bp.route('/camera')
def camera():
    return render_template('camera.html')


@bp.route('/logs')
def logs():
  return render_template('logs.html')

@bp.route('/show_env')
def show_env():
    return render_template('show_env.html')