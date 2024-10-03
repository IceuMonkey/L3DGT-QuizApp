from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify 
from .models import Question
from ..database import db
import random

quiz_bp = Blueprint('quiz', __name__, template_folder='../templates')
quiz = quiz_bp

@quiz.route('/quiz', methods=['GET', 'POST'])
def quiz_view():
    # Initialise Quiz
    if 'question_ids' not in session:
        session['question_ids'] = [q.id for q in Question.query.all()] # Get all question IDs from the database
        random.shuffle(session['question_ids']) # Shuffle thier order
        # Initialise Session variables
        session['correct_streak'] = 0 
        session['best_streak'] = 0

    # When there are no more questions, reshuffles questions and redirect to results page
    if not session['question_ids']:
        print("No Questions!") # Debug: Prints when session has run out of questions
        # Reshuffles questions back into session
        session['question_ids'] = [q.id for q in Question.query.all()]
        random.shuffle(session['question_ids'])
        return redirect(url_for('quiz.result'))


    question_id = session['question_ids'].pop() # Pop/Remove a question ID from the list and get the corresponding question from the database
    session['current_question_id'] = question_id # Stores the popped question as the current question in the session
    question = Question.query.get(question_id) 
    return render_template('quiz.html', question=question) # Renders Quiz template with current question

@quiz.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.get_json() # Get the submitted answer from the request data
    selected_answer = data.get('answer') 
    question_id = session.get('current_question_id') # Get the current question ID from the session
    question = Question.query.get(question_id)
    
    if selected_answer == question.answer: # If answer is correct
        session['correct_streak'] += 1 # Tracks Streak for Current Quiz
        # If current streak is better than the best streak, set best_streak to the current streak
        if session['correct_streak'] > session['best_streak']:
            session['best_streak'] = session['correct_streak']
        # If there are no more questions, return 'end' result
        if not session['question_ids']:
            print("No more Questions!") # Debug: Prints when session has run out of questions
            return jsonify({'result': 'end'})
        return jsonify({'result': 'correct'}) # Returns "Correct" result
    else: # Resets current streak and return wrong result
        print("Wrong Answer!")
        session['correct_streak'] = 0
        return jsonify({'result': 'wrong'})

@quiz.route('/result')
def result():
    # Gets answer_streak data from session data
    correct_streak = session.get('correct_streak', 0)
    best_streak = session.get('best_streak', 0)

    # Renders Results page
    return render_template('quizresult.html', correct_streak=correct_streak, best_streak=best_streak)
