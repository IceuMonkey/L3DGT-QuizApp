# SCRIPT TO ADD QUESTIONS TO QUIZ DB
from website import create_app
from website.database import db
from website.quiz.models import Question

app = create_app()

# New Questions are stored as dictionaries
# Questions list
questions = [
    {
        "question_text": "What is the primary ingredient in guacamole?",
        "answer": "Avocado",
        "options": ["Tomato", "Avocado", "Onion", "Pepper"]
    },
    {
        "question_text": "Who was the first person to walk on the moon?",
        "answer": "Neil Armstrong",
        "options": ["Buzz Aldrin", "Yuri Gagarin", "Neil Armstrong", "Michael Collins"]
    },
    {
        "question_text": "What is the main language spoken in Brazil?",
        "answer": "Portuguese",
        "options": ["Spanish", "Portuguese", "French", "English"]
    },
    {
        "question_text": "What is the currency of Japan?",
        "answer": "Yen",
        "options": ["Yuan", "Won", "Yen", "Dollar"]
    },
    {
        "question_text": "Who is the author of the Harry Potter series?",
        "answer": "J.K. Rowling",
        "options": ["J.K. Rowling", "J.R.R. Tolkien", "George R.R. Martin", "C.S. Lewis"]
    },
    {
        "question_text": "What is the largest bone in the human body?",
        "answer": "Femur",
        "options": ["Tibia", "Femur", "Humerus", "Fibula"]
    },
    {
        "question_text": "What is the capital of Thailand?",
        "answer": "Bangkok",
        "options": ["Bangkok", "Hanoi", "Jakarta", "Manila"]
    },
    {
        "question_text": "Who painted 'The Persistence of Memory'?",
        "answer": "Salvador Dalí",
        "options": ["Pablo Picasso", "Salvador Dalí", "Henri Matisse", "Claude Monet"]
    },
    {
        "question_text": "What is the smallest bone in the human body?",
        "answer": "Stapes",
        "options": ["Stapes", "Ulna", "Patella", "Scapula"]
    },
    {
        "question_text": "What is the national flower of Japan?",
        "answer": "Cherry Blossom",
        "options": ["Lotus", "Rose", "Cherry Blossom", "Tulip"]
    },
    {
        "question_text": "Who invented the World Wide Web?",
        "answer": "Tim Berners-Lee",
        "options": ["Bill Gates", "Steve Jobs", "Tim Berners-Lee", "Mark Zuckerberg"]
    },
    {
        "question_text": "What is the capital of South Africa?",
        "answer": "Pretoria",
        "options": ["Cape Town", "Johannesburg", "Pretoria", "Durban"]
    },
    {
        "question_text": "What is the most spoken language in the world?",
        "answer": "Mandarin Chinese",
        "options": ["English", "Spanish", "Hindi", "Mandarin Chinese"]
    },
    {
        "question_text": "Who wrote 'The Iliad'?",
        "answer": "Homer",
        "options": ["Homer", "Virgil", "Sophocles", "Euripides"]
    },
    {
        "question_text": "What is the capital of Mexico?",
        "answer": "Mexico City",
        "options": ["Guadalajara", "Monterrey", "Mexico City", "Cancun"]
    },
    {
        "question_text": "What is the chemical symbol for potassium?",
        "answer": "K",
        "options": ["P", "K", "Pt", "Po"]
    },
    {
        "question_text": "Who wrote 'The Hobbit'?",
        "answer": "J.R.R. Tolkien",
        "options": ["J.K. Rowling", "J.R.R. Tolkien", "George R.R. Martin", "C.S. Lewis"]
    },
    {
        "question_text": "What is the capital of Norway?",
        "answer": "Oslo",
        "options": ["Stockholm", "Copenhagen", "Oslo", "Helsinki"]
    },
    {
        "question_text": "What is the largest organ in the human body?",
        "answer": "Skin",
        "options": ["Liver", "Heart", "Skin", "Lungs"]
    }
]


with app.app_context():
    for q in questions:
        existing_question = Question.query.filter_by(question_text=q["question_text"]).first() # Query checks if the question already exists in db 
        if existing_question is None: # Adds questions that do not exist
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