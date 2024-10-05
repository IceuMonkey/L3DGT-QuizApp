# SCRIPT TO ADD QUESTIONS TO QUIZ DB
from website import create_app
from website.database import db
from website.quiz.models import Question

app = create_app()

questions = [
    {
        "question_text": "What is the smallest country in the world?",
        "answer": "Vatican City",
        "options": ["Monaco", "Vatican City", "San Marino", "Liechtenstein"]
    },
    {
        "question_text": "What is the chemical symbol for gold?",
        "answer": "Au",
        "options": ["Ag", "Au", "Pb", "Fe"]
    },
    {
        "question_text": "Who wrote 'To Kill a Mockingbird'?",
        "answer": "Harper Lee",
        "options": ["Harper Lee", "Mark Twain", "Ernest Hemingway", "F. Scott Fitzgerald"]
    },
    {
        "question_text": "What is the tallest mountain in the world?",
        "answer": "Mount Everest",
        "options": ["K2", "Kangchenjunga", "Lhotse", "Mount Everest"]
    },
    {
        "question_text": "Which element has the atomic number 1?",
        "answer": "Hydrogen",
        "options": ["Helium", "Hydrogen", "Oxygen", "Carbon"]
    },
    {
        "question_text": "What is the longest river in the world?",
        "answer": "Nile",
        "options": ["Amazon", "Nile", "Yangtze", "Mississippi"]
    }
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