from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_heroku import Heroku

app = Flask(__name__)
#heroku = Heroku(app)

app.config.from_pyfile('config.py')
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db = SQLAlchemy(app)

from views import *

if __name__ == "__main__":
	#heroku.init_app(app)
	#app.run_server(debug=True)
	app.run(debug=True)
