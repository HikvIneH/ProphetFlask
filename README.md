Analison
===================
can't find any proper name yet

Flask using fbprophet to run time-series prediction.

This is it.

I used fix-yahoo-finance to get yahoo historical data [ranaroussi](https://github.com/ranaroussi).
and for predicting time-series, I used prophet from [facebook](https://facebook.github.io/prophet) with graph from [dygraph](https://github.com/danvk/dygraphs).

There are probably better ways to do this.


Running it
=================
pip install the requirements:

```
pip install -r requirements.txt
```

export your configs:

```
export FLASK_APP=run.py
export FLASK_CONFIG=development
```

you can create an instance folder with your SQLAlchemy config:
```
export SQLALCHEMY_DATABASE_URI='your database'
export SECRET_KEY='yoursecretkey'
```

And then just run the server to check it out in your browser:

```
python run.py
```
or with gunicorn

```
gunicorn run:app
```
