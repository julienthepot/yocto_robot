import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from web.db import get_db

bp = Blueprint('camera', __name__, url_prefix='/')


@bp.route('/camera')
def camera():
    return render_template('camera.html')

@bp.route('/stream.mjpeg')
def stream_mjpeg():
  from flask import Response
  import websocket
  import sys

  def gen():
    ws = None
    try:
      ws = websocket.create_connection("ws://192.168.1.146:8765/video", timeout=5)
      boundary = b'--frame\r\n'
      while True:
        msg = ws.recv()
        if msg is None:
          break
        if isinstance(msg, str):
          # ignore initial info text message
          continue
        yield boundary
        yield b'Content-Type: image/jpeg\r\nContent-Length: %d\r\n\r\n' % len(msg)
        yield msg
        yield b'\r\n'
    except Exception:
      pass
    finally:
      if ws:
        try:
          ws.close()
        except Exception:
          pass

  return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

