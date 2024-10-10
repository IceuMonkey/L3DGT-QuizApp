# quiz.py
from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify
from flask_login  import login_required
from .models import Question
from ..auth.models import users
from ..database import db
import random

quiz_bp = Blueprint('quiz', __name__, template_folder='../templates')
quiz = quiz_bp

# Time allowed to answer question per dificulty 
difficulty_time_limits = {
    1: 15, # Easy
    2: 10, # Medium
    3: 5,  # Hard
    4: 3, # Extreme
}

@quiz.route('/quiz', methods=['GET', 'POST'])
def quiz_view():
    # Initialise Quiz
    if 'question_ids' not in session: # If no question_ids key are in session
        session['question_ids'] = [q.id for q in Question.query.all()] # Get all question IDs from the database
        random.shuffle(session['question_ids']) # Shuffles their order
        # Initialise Session variables
        user = users.query.filter_by(id=session['user_id']).first()
        session['correct_streak'] = 0 
        session['best_streak'] = user.best_streak
        
    # When there are no more questions (i.e user ran out of questions), reshuffles questions and reloads page
    if not session['question_ids']:
        print("No Questions!") # Debug: Prints when session has run out of questions
        # Reshuffles questions back into session
        session['question_ids'].pop
        session['question_ids'] = [q.id for q in Question.query.all()]
        random.shuffle(session['question_ids'])
        return redirect(url_for('quiz.result'))

    # Gets current Question
    question_id = session['question_ids'].pop() # Pop/Remove a question ID from the list and get the corresponding question from the database
    session['current_question_id'] = question_id # Stores the popped question as the current question in the session
    question = Question.query.get(question_id) 

    # Shuffle Answer Options
    options = question.options # Gets current question's options as variable
    random.shuffle(options) # Shuffles their order
    question.options = options # Updates the current question's option's with the shuffled options 

    # Time to answer question (quiz difficutly)
    user = users.query.filter_by(id=session['user_id']).first()
    time_limit = difficulty_time_limits.get(user.difficulty, 10) 

    return render_template('quiz.html', question=question, time_limit=time_limit) # Renders Quiz template with current question

@quiz.route('/submit_answer', methods=['POST'])
@login_required
def submit_answer():
    if 'user_id' not in session:
        print("User Id not in Session") # Debug
        return redirect(url_for('auth.login'))  # Redirect to login page if user_id is not in session

    print(f"User ID in session: {session['user_id']}")  # Debug
    data = request.get_json() # Get the submitted answer from the request data
    selected_answer = data.get('answer') 
    question_id = session.get('current_question_id') # Get the current question ID from the session
    question = Question.query.get(question_id)
    
    if selected_answer == question.answer: # If answer is correct
        session['correct_streak'] += 1 # Tracks Streak for Current Quiz
        user = users.query.filter_by(id=session['user_id']).first()
        
        if user: # If user found in db, increment total_solved
            user.total_solved = (user.total_solved or 0) + 1 # Checks total_solved is not None before incrementing
            db.session.commit()
        
        if session['correct_streak'] > session['best_streak']: # If current streak is better than the best streak, set best_streak to the current streak
            session['best_streak'] = session['correct_streak']
            # Updating Best Streak and Total Solved in DB
            if user:
                user.best_streak = session['best_streak']
                db.session.commit()
        # If there are no more questions, return 'end' result
        
        if not session['question_ids']:
            print("No more Questions!") # Debug: Prints when session has run out of questions
            return jsonify({'result': 'end'})
        return jsonify({'result': 'correct'}) # Returns "Correct" result
    else: # Return wrong result
        print("Wrong Answer!")
        return jsonify({'result': 'wrong'})

@quiz.route('/result')
def result():
    # Gets current answer_streak from session data
    correct_streak = session.get('correct_streak', 0)

    # Gets all time best answer_streak and total questions solved from users db 
    user = users.query.filter_by(id=session['user_id']).first()
    best_streak = user.best_streak if user else 0
    total_solved = user.total_solved if user else 0

    # Reinitialise Quiz
    print("Resetting Quiz!")
    session['correct_streak'] = 0
    session['question_ids'].pop
    session['question_ids'] = [q.id for q in Question.query.all()]
    random.shuffle(session['question_ids'])

    # Renders Results page
    return render_template('quizresult.html', correct_streak=correct_streak, best_streak=best_streak, total_solved=total_solved)
