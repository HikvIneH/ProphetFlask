from app import app, db

from flask import render_template, flash, request, jsonify, redirect, url_for, session, g
from forms import RegistrationForm, LoginForm
from model import User

from passlib.hash import sha256_crypt

import pandas as pd
import numpy as np
from fbprophet import Prophet
import datetime
import os
import os.path
import math as math
import csv
from math import sqrt
from itertools import izip_longest

import fix_yahoo_finance as yf
import pandas as pd
import datetime

@app.before_request
def before_request():
	g.user = None
	if 'user' in session:
		g.user = session['user']

@app.after_request
def add_header(response):
	"""
	Add headers to both force latest IE rendering engine or Chrome Frame,
	and also to cache the rendered page for 10 minutes.
	"""
	response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
	response.headers['Cache-Control'] = 'public, max-age=0'
	return response

@app.route('/', methods=['GET','POST'])
def homepage():
	if not g.user:
		return render_template('welcome.html')
	if request.method == 'POST':
		stock = request.form['companyname']
		start = datetime.datetime(2010, 1, 4).date()
		end = datetime.datetime.now().date()
		'''
		if os.path.isfile("./static/data/"+stock+'-'+str(startDate)+'to'+str(endDate)+".csv") == False: 
			df_historical = pd.read_csv("./static/data/"+stock+'-'+str(startDate)+'to'+str(endDate)+".csv")
			df_historical.round(3)
		else:
			df_historical = yf.download(stock, startDate, endDate)
			df_historical.to_csv("./static/data/"+stock+'-'+str(startDate)+'to'+str(endDate)+".csv")
			df_historical.round(3)
		'''
		df_historical = yf.download(stock, start, end)
		df = df_historical.filter(['Close'])
		
		df['ds'] = df.index
		df['y'] = np.log(df['Close'])
		original_end = df['Close'][-1]

		
		model = Prophet()
		model.fit(df)

		num_days = 7
		future = model.make_future_dataframe(periods=num_days)
		forecast = model.predict(future)
		
		print (forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

		#make the vizualization a little better to understand
		df.set_index('ds', inplace=True)
		forecast.set_index('ds', inplace=True)
		#date = df['ds'].tail(plot_num)
		
		p_df = df.join(forecast[['yhat', 'yhat_lower','yhat_upper']], how = 'outer')
		p_df['yhat_scaled'] = np.exp(p_df['yhat'])

		close_data = p_df.Close
		forecasted_data = p_df.yhat_scaled
		date = future['ds']
		#date = p_df.index[-plot_num:-1]
		forecast_start = forecasted_data[-1]
		forecast_future = forecasted_data[-8]
		
		#y_hatx = np.exp(p_df['yhat']['2018-10-25':])
		#y_hat = np.exp(p_df['yhat'][-8:])
		


		d = [date, close_data, forecasted_data]
		export_data = izip_longest(*d, fillvalue = '')
		with open('./static/data/prediction.csv', 'wb') as myfile:
			wr = csv.writer(myfile)
			wr.writerow(("Date", "Actual", "Forecasted"))
			wr.writerows(export_data)
		myfile.close()  

		#return render_template("visual.html", original = round(original_end,2), forecast = round(forecast_start,2), stock_tinker = stock.upper())
		return render_template("prediction.html", original = round(original_end,2), forecast = round(forecast_start,2),forecast_future = round(forecast_future,2), stock_tinker = stock.upper(), num_days=num_days)
	return render_template('homepage.html')

@app.route('/login', methods=['GET','POST'])
def login():
	error = None
	try:
		form = LoginForm(request.form)
		
		if request.method == 'POST' and form.validate():
			user = form.username.data
			result = User.query.filter_by(username= user).first()
			if result is not None:
				if sha256_crypt.verify(form.password.data, result.password):
					session['user'] = user
					return redirect(url_for('homepage'))
				else:
					error = "password not valid."
			else:
				error = "User doesn't exist."
				
		return render_template('login.html', form=form, error = error)
	except Exception as e:
		return render_template('login.html', form=form, error = e)
	

@app.route('/logout')
def logout():
	session.pop('user', None)
	return redirect(url_for('homepage'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	error = None
	try:	
		form = RegistrationForm(request.form)
		
		if request.method == 'POST' and form.validate():
			username = form.username.data
			email = form.email.data
			password = sha256_crypt.encrypt((str(form.password.data)))
			### validate email address
			newuser = User(username=username, email=email, password=password)
			db.session.add(newuser)
			db.session.commit()
			session['user'] = username
			flash("Successfully registered in!", 'success')
			return redirect(url_for('homepage'))
		return render_template('register.html', form=form)

	except Exception as e:
		# if e is database error 
		return render_template('register.html', form=form, error = e)


@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')

# ------------------------------------------------------ error handle
@app.errorhandler(404)
def page_not_found(e):
	return "Woops! page not found!"

@app.errorhandler(405)
def method_not_found(e):
	return "Woops! method doesn't exist!"

#------------------------------------------------------- Prophet

##@app.route("/visual" , methods = ['POST', 'GET'])
  

