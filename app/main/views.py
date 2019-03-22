from flask import render_template, request, flash
from flask_login import login_required, current_user

from . import main
from forms import DashboardForm
from forms import UploadForm

from .. import db
from werkzeug.utils import secure_filename
from ..models import Data

import pandas as pd
import numpy as np
from fbprophet import Prophet
import datetime
import os
import os.path
import math as math
import csv
from math import sqrt
from sklearn.metrics import mean_squared_error

#from itertools import izip_longest
import pickle

import fix_yahoo_finance as yf
import pandas as pd
import datetime


@main.route('/dashboard')
@main.route('/dashboard/')
@main.route('/')
def dashboard():     
	return render_template('main/index.html', title="Welcome")

@main.route('/dashboard/predict', methods=['GET','POST'])
@main.route('/dashboard/predict/', methods=['GET','POST'])
@login_required
def analyzeFromYahoo():
	form = DashboardForm(csrf_enabled=False)
	if form.validate_on_submit():
	#if request.method == 'POST':
		#stock = request.form['companyname']
		stock=form.stock.data.upper()
		num_days=form.num_days_ahead.data
		num_days_back=form.num_days_back.data
		#startDate = datetime.datetime(2010, 1, 4).date()
		endDate = datetime.datetime.now().date()
		startDate = datetime.datetime.strptime(str(endDate), '%Y-%m-%d').date() - datetime.timedelta(days=num_days_back)
		sekarang = str(startDate)+"-TO-"+str(endDate)+"-"
		current = str(num_days)+"-TO-"+str(num_days_back)+"-ON-"+str(endDate)

		while os.path.isfile("./app/static/data/yahoostocks/"+current+stock+".csv") == False: 
			try: 
				df_historical = yf.download(stock, startDate, endDate)
				df_historical.to_csv("./app/static/data/yahoostocks/"+current+stock+".csv")
				print 'success'
				break
			except ValueError:
				flash('Yahoo Finance could not process your request. Please try again.','warning')
				print 'error'
				return render_template('main/predict.html',form=form, title='Predict from Yahoo Finance')
		else:
			df_historical = pd.read_csv("./app/static/data/yahoostocks/"+current+stock+".csv", index_col=[0])
			print 'previous searched csv used'
					
		#df_historical = yf.download(stock, startDate, endDate)
		
		df = df_historical.filter(['Close'])
		df['ds'] = df.index
		df['y'] = np.log(df['Close'])
		original_end = df['Close'][-1]
		
		#model = Prophet(weekly_seasonality=True, dail y_seasonality=True, yearly_seasonality=True)
		'''
		if os.path.isfile("./app/static/data/pickles/"+current+stock+"-pickle.pckl") == True: 
			with open("./app/static/data/pickles/"+current+stock+"-pickle.pckl", "rb") as f:
				model = pickle.load(f)
				print 'Model Opened'            
		else:
			model = Prophet(daily_seasonality=False, weekly_seasonality=True ,yearly_seasonality=True)
			model.fit(df)
			with open("./app/static/data/pickles/"+current+stock+"-pickle.pckl", "wb") as f:
				pickle.dump(model, f)
		'''

		model = Prophet(daily_seasonality=False, weekly_seasonality=True ,yearly_seasonality=True)
		model.fit(df)

		#num_days = 7
		future = model.make_future_dataframe(periods=num_days)
		forecast = model.predict(future)
	
		print (forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].head())

		df.set_index('ds', inplace=True)
		forecast.set_index('ds', inplace=True)

		p_df = df.join(forecast[['yhat', 'yhat_lower','yhat_upper']], how = 'outer')
		p_df['yhat_scaled'] = np.exp(p_df['yhat'])

		close_data = p_df.Close
		forecasted_data = p_df.yhat_scaled
		date = future['ds']
		#date = p_df.index[-plot_num:-1]
		forecast_start = forecasted_data[-1]
		forecast_future = forecasted_data[-(int(num_days)+1)]

		rmse1 = p_df.iloc[:-num_days:30]
		print "rmse = " + str(rmse1)
		rmse = round(sqrt(mean_squared_error(rmse1.Close,rmse1.yhat_scaled , multioutput='raw_values')),4)
		print rmse
		#y_hatx = np.exp(p_df['yhat']['2018-10-25':])
		#y_hat = np.exp(p_df['yhat'][-8:])
		'''
		d = [date, close_data, forecasted_data]
		export_data = izip_longest(*d, fillvalue = '')
		print export_data
		
		with open('./app/static/data/predictions/'+sekarang+stock+'-'+str(num_days)+'-prediction.csv', 'wb') as myfile:
			wr = csv.writer(myfile)
			wr.writerow(("Date", "Actual", "Forecasted"))
			wr.writerows(export_data)
		#myfile.close()  
		'''
		date = pd.DataFrame(date)
		close_data = pd.DataFrame(close_data)
		forecasted_data = pd.DataFrame(forecasted_data)
		
		plotFile = close_data.join(forecasted_data, how = 'outer')
		plotFile = plotFile.rename(index=str, columns={"Close": "Actual", "yhat_scaled": "Forecasted"})
		plotFile.index.names = ['date']
		plotFile.tail()
		plotFile.to_csv('./app/static/data/predictions/predict/'+current+stock+'-'+str(num_days)+'-prediction.csv', na_rep='nan')

		return render_template("main/plot.html", original = round(original_end,2), 
								forecast = round(forecast_start,2),
								forecast_future = round(forecast_future,2),
								stock_tinker = stock.upper(),
								RMSE = rmse,
								num_days=num_days,sekarang=sekarang,current=current,
								title='forecasting result of '+stock
								)
	return render_template('main/predict.html',form=form, title='Predict from Yahoo Finance')

@main.route('/dashboard/explore', methods=['GET','POST'])
@main.route('/dashboard/explore/', methods=['GET','POST'])
@login_required
def analyzeManually():
	form = UploadForm(csrf_enabled=False)
	if form.validate_on_submit():
		f = form.data.data
		filename = secure_filename(f.filename)
		#filename = 'UPLOADEDBY-'+str(current_user.username).upper()
		daily = form.dailySeasonality.data
		weekly = form.weeklySeasonality.data
		yearly = form.yearlySeasonality.data
		num_days = form.num_days_ahead.data
		change = form.change.data
		endDate = datetime.datetime.now().date()
		print filename, daily, weekly, yearly, num_days

		'''
		if True:
			try:
				df_historical = pd.read_csv(f, index_col=[0])
				if 'Target' in list(df_historical):
					df = df_historical.filter(['Target'])
					print 'target in list'
				else:
					flash('Change your csv header to Target','danger')
					return render_template('main/explore.html', form=form, title='Upload csv')
			except pd.errors.EmptyDataError as e:
				flash(e,'danger')
				return render_template('main/explore.html', form=form, title='Upload csv')
		'''

		df_historical = pd.read_csv(f, index_col=[0])
		try:
			if change in list(df_historical):
				df = df_historical.rename(columns={change :'Target'})
			else:
				flash('No such a column ' + change + '! Please review your file', 'danger')
				return render_template('main/explore.html', form=form, title='Upload csv')
		except pd.errors.EmptyDataError as e:
			flash(e,'danger')
			return render_template('main/explore.html', form=form, title='Upload csv')
		
		#df_historical = pd.read_csv(f, index_col=[0])
		#df = pd.DataFrame(data=df_historical)
		#df = df_historical.filter(['Target'])
		
		df['ds'] = df.index
		df['y'] = np.log(df['Target'])
		#df['y'] = np.log(df[-1])
		original_end = df['Target'][-1]
		#model = Prophet(daily_seasonality=daily, weekly_seasonality=weekly, yearly_seasonality=yearly)
		model = Prophet()
		model.fit(df)

		future = model.make_future_dataframe(periods=num_days)
		forecast = model.predict(future)
	
		print (forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

		df.set_index('ds', inplace=True)
		forecast.set_index('ds', inplace=True)

		p_df = df.join(forecast[['yhat', 'yhat_lower','yhat_upper']], how = 'outer')
		p_df['yhat_scaled'] = np.exp(p_df['yhat'])

		close_data = p_df.Target
		forecasted_data = p_df.yhat_scaled
		date = future['ds']
		# date = p_df.index[-plot_num:-1]
		forecast_start = forecasted_data[-1]
		forecast_future = forecasted_data[-(int(num_days)+1)]

		rmse1 = p_df.iloc[:-num_days:60]
		print "rmse = " + str(rmse1)
		rmse = round(sqrt(mean_squared_error(rmse1.Target,rmse1.yhat_scaled , multioutput='raw_values')),4)
			
		# y_hatx = np.exp(p_df['yhat']['2018-10-25':])
		# y_hat = np.exp(p_df['yhat'][-8:])
		date = pd.DataFrame(date)
		close_data = pd.DataFrame(close_data)
		forecasted_data = pd.DataFrame(forecasted_data)

		plotFile = close_data.join(forecasted_data, how = 'outer')
		plotFile = plotFile.rename(index=str, columns={"Target": "Actual", "yhat_scaled": "Forecasted"})
		plotFile.index.names = ['date']
		plotFile.tail()
		plotFile.to_csv('./app/static/data/predictions/explore/'+str(filename).upper()+str(num_days)+'-prediction.csv', na_rep='nan')

		# newFile = Data(name=f.filename, data=f.read(), user_id=current_user.id)
		# db.session.add(newFile)
		# db.session.commit()

		print rmse
		print original_end
		print forecast_start
		

		return render_template("main/plot_explore.html", original = round(original_end,2), 
								forecast = round(forecast_start,2), RMSE = rmse,
								forecast_future = round(forecast_future,2),
								filename = filename.upper(),
								change = change,
								num_days=num_days, title='forecasting result of ' + filename + '' + change
								)
	return render_template('main/explore.html', form=form, title='Upload csv')
