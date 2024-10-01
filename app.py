from website import create_app # From __init__ file

app = create_app()

if __name__ == "__main__":
    app.run(debug=True) # debug=True will automatically reload dev server when a change to the code is detected