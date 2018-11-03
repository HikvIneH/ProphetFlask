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
		startDate = datetime.datetime(2013, 1, 4).date()
		endDate = datetime.datetime.now().date()

		df_historical = yf.download(stock, startDate, endDate)
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

		df.set_index('ds', inplace=True)
		forecast.set_index('ds', inplace=True)

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
		
		with open('./app/static/data/prediction.csv', 'wb') as myfile:
			wr = csv.writer(myfile)
			wr.writerow(("Date", "Actual", "Forecasted"))
			wr.writerows(export_data)
		myfile.close()  
		#return render_template("visual.html", original = round(original_end,2), forecast = round(forecast_start,2), stock_tinker = stock.upper())
		return render_template("home/dashboard-predict.html", original = round(original_end,2), forecast = round(forecast_start,2),forecast_future = round(forecast_future,2), stock_tinker = stock.upper(), num_days=num_days)
	return render_template('home/dashboard.html')