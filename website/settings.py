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
        dark_mode = 'dark' if request.form.get('dark_mode') else 'light'        

        # Get the current User
        user = users.query.filter_by(id=session['user_id']).first()
        
        if user:
            # Update Found USer Settings
            user.difficulty = int(difficulty)
            user.theme = dark_mode
            db.session.commit()

        return redirect(url_for('settings.settings'))

    # Get the current User
    user = users.query.filter_by(id=session['user_id']).first()

    # Prepopulate with current settings
    current_difficulty = user.difficulty if user else 2  # Default to 'Medium' (difficulty 2)
    current_theme = user.theme if user else 'dark'  # Default to 'dark' theme

    return render_template('settings.html', current_difficulty=current_difficulty, current_theme=current_theme)