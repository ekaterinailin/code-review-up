from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'This is the homepage'

@app.route('/Ahmed')
def Ahmed():
    return '<h2>Ahmed is a goodperson</h2>'


if __name__ == "__main__":
    app.run(debug=True)
    


