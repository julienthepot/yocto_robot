import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from web.db import get_db

bp = Blueprint('show_env', __name__, url_prefix='/')
