# SCRIPT TO ADD QUESTIONS TO QUIZ DB
from website import create_app
from website.database import db
from website.quiz.models import Question

app = create_app()

questions = [
    {
        "question_text": "What is the capital of France?",
        "answer": "Paris",
        "options": ["Paris", "London", "Madrid", "Rome"]
    },
    {
        "question_text": "Which planet is known as the Red Planet?",
        "answer": "Mars",
        "options": ["Earth", "Mars", "Saturn", "Venus"]
    },
    {
        "question_text": "What is the largest planet in our solar system?",
        "answer": "Jupiter",
        "options": ["Earth", "Mars", "Jupiter", "Saturn"]
    },    
    {
        "question_text": "Who painted the Mona Lisa?",
        "answer": "Leonardo da Vinci",
        "options": ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Claude Monet"]
    },
]

with app.app_context():
    for q in questions:
        existing_question = Question.query.filter_by(question_text=q["question_text"]).first() # Query checks if the question already exists in db 
        if existing_question is None: # For questions that do not exist
            new_question = Question(
                question_text=q["question_text"],
                answer=q["answer"],
                options=q["options"]
            )
            db.session.add(new_question)
    db.session.commit()
    print("Questions added successfully!")


### QUESTION FORMAT
    # {
    #     "question_text": "",
    #     "answer": "",
    #     "options": ["", "", "", ""]
    # },