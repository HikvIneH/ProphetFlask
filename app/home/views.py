from flask import render_template, request
from flask_login import login_required, current_user

from . import home

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
import pickle

import fix_yahoo_finance as yf
import pandas as pd
import datetime


@home.route('/')
def homepage():     
	return render_template('home/index.html', title="Welcome")

@home.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
	if request.method == 'POST':
		stock = request.form['companyname']
		startDate = datetime.datetime(2010, 1, 4).date()
		endDate = datetime.datetime.now().date()
		sekarang = str(startDate)+"-TO-"+str(endDate)+"-"

		if os.path.isfile("./app/static/data/yahoostocks/"+sekarang+stock+".csv") == False: 
			df_historical = yf.download(stock, startDate, endDate)
			df_historical.to_csv("./app/static/data/yahoostocks/"+sekarang+stock+".csv")			            
		else:
			df_historical = pd.read_csv("./app/static/data/yahoostocks/"+sekarang+stock+".csv", index_col=[0])
			print 'DataFrame Opened'

		#df_historical = yf.download(stock, startDate, endDate)
		df = df_historical.filter(['Close'])
		
		df['ds'] = df.index
		df['y'] = np.log(df['Close'])
		original_end = df['Close'][-1]

		#model = Prophet(weekly_seasonality=True, dail y_seasonality=True, yearly_seasonality=True)
		if os.path.isfile("./app/static/data/pickles/"+sekarang+stock+"-pickle.pckl") == True: 
			with open("./app/static/data/pickles/"+sekarang+stock+"-pickle.pckl", "rb") as f:
				model = pickle.load(f)
				print 'Model Opened'            
		else:
			model = Prophet()
			model.fit(df)
			with open("./app/static/data/pickles/"+sekarang+stock+"-pickle.pckl", "wb") as f:
				pickle.dump(model, f)


		#model = Prophet()
		#model.fit(df)

		num_days = 30
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
		forecast_future = forecasted_data[-31]
		
		#y_hatx = np.exp(p_df['yhat']['2018-10-25':])
		#y_hat = np.exp(p_df['yhat'][-8:])
		
		d = [date, close_data, forecasted_data]
		export_data = izip_longest(*d, fillvalue = '')
		
		with open('./app/static/data/predictions/'+sekarang+stock+'-prediction.csv', 'wb') as myfile:
			wr = csv.writer(myfile)
			wr.writerow(("Date", "Actual", "Forecasted"))
			wr.writerows(export_data)
		#myfile.close()  

		return render_template("home/dashboard-predict.html", original = round(original_end,2), forecast = round(forecast_start,2),forecast_future = round(forecast_future,2), stock_tinker = stock.upper(), num_days=num_days,sekarang=sekarang )
	return render_template('home/dashboard.html')