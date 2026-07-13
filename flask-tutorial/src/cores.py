from flask import Blueprint, render_template, request, redirect, url_for
from .db import get_db

bp = Blueprint('cores', __name__)


@bp.route('/')
def index():
    db = get_db()
        colors = db.execute(
                'SELECT * FROM color'
                    ).fetchall()

                        return render_template('cores/index.html', colors=colors)