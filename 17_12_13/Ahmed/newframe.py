
from flask import Flask
app = Flask(__name__)

# @ signifies a decorator - way to wrap a function  and modifying its  behovior
@app.route('/')
def index():
    return 'This is the home page.'

	
@app.route('/Ahmed')
def Ahmed():
    return '<h2>Ahmed is good</h2>'
	
	
@app.route('/profile/<username>')
def profile(username):
    return "<h2>Hey friend how are you %s<h2>" % username
	
	
if __name__ == "__main__":
    app.run()
   