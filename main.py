from website import app # From __init__ file

2
if __name__ == "__main__":
    with app.app_context(): 
        from website.models import db
        db.create_all() # Initialises DB on start up before running app
    app.run(debug=True) # debug=True will automatically reload dev server when a change to the code is detected