from flask import Blueprint, render_template, redirect, session, request, url_for
from flask_login import login_required
from .database import db
from .auth.models import users

settings_bp = Blueprint('settings', __name__)
settings = settings_bp

@settings.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        difficulty = request.form.get('difficulty')
        user = users.query.filter_by(id=session['user_id']).first()
        if user:
            user.difficulty = int(difficulty)
            db.session.commit()
        return redirect(url_for('settings.settings'))

    user = users.query.filter_by(id=session['user_id']).first()
    current_difficulty = user.difficulty if user else 2
    return render_template('settings.html', current_difficulty=current_difficulty)