import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from web.db import get_db
from flask import jsonify

bp = Blueprint('log', __name__, url_prefix='/log')

@bp.route('/logs')
def get_all_logs():
  db = get_db()
  logs = db.execute(
    'SELECT id, created, level, message FROM log ORDER BY created DESC'
  ).fetchall()
  return jsonify([dict(log) for log in logs])

@bp.route('/add', methods=['POST'])
def add_log():
  level = request.form.get('level', 'INFO')
  message = request.form.get('message')
  created = request.form.get('created')
  
  db = get_db()
  db.execute(
    'INSERT INTO log (created, level, message) VALUES (?, ?, ?)',
    (created, level, message)
  )
  db.commit()
  
  return jsonify({'status': 'success'}), 200