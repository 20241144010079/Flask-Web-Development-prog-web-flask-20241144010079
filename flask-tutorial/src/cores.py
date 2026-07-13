from flask import Blueprint, render_template, request, redirect, url_for
from .db import get_db
from .auth import login_required

bp = Blueprint('cores', __name__)


@bp.route('/')
def index():
    db = get_db()

    colors = db.execute(
        'SELECT * FROM color'
    ).fetchall()

    return render_template('cores/index.html', colors=colors)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        hex_color = request.form['hex']
        description = request.form['description']

        db = get_db()

        db.execute(
            '''
            INSERT INTO color (name, hex, description)
            VALUES (?, ?, ?)
            ''',
            (name, hex_color, description)
        )

        db.commit()

        return redirect(url_for('cores.index'))

    return render_template('cores/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    db = get_db()

    color = db.execute(
        'SELECT * FROM color WHERE id = ?',
        (id,)
    ).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        hex_color = request.form['hex']
        description = request.form['description']

        db.execute(
            '''
            UPDATE color
            SET name = ?, hex = ?, description = ?
            WHERE id = ?
            ''',
            (name, hex_color, description, id)
        )

        db.commit()

        return redirect(url_for('cores.index'))

    return render_template('cores/update.html', color=color)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    db = get_db()

    db.execute(
        'DELETE FROM color WHERE id = ?',
        (id,)
    )

    db.commit()

    return redirect(url_for('cores.index'))