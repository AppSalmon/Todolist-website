from todolist import *

app = create_app()

@app.route('/test')
def home():
    return "Hahaha you is chicken🐣"


if __name__ == "__main__":
    app.run(debug = True)