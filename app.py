from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db = SQLAlchemy(app)

from views import *

if __name__ == "__main__":
	app.run_server(debug=True)
	#app.run(host='localhost',port=3000)