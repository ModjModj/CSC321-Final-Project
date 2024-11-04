from __init__ import create_app
#Create the web application
if __name__ == "__main__":
    app = create_app()
    app.run(debug = True)