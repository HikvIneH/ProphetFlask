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
		print filename, daily, weekly, yearly, num_days

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

		#df_historical = pd.read_csv(f, index_col=[0])
		df = pd.DataFrame(data=df_historical)
		#df = df_historical.filter(['Target'])
		
		df['ds'] = df.index
		df['y'] = np.log(df['Target'])
		#df['y'] = np.log(df[-1])
		original_end = df['Target'][-1]
		model = Prophet(daily_seasonality=daily, weekly_seasonality=weekly, yearly_seasonality=yearly)
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
		#date = p_df.index[-plot_num:-1]
		forecast_start = forecasted_data[-1]
		forecast_future = forecasted_data[-(int(num_days)+1)]
			
		#y_hatx = np.exp(p_df['yhat']['2018-10-25':])
		#y_hat = np.exp(p_df['yhat'][-8:])
		date = pd.DataFrame(date)
		close_data = pd.DataFrame(close_data)
		forecasted_data = pd.DataFrame(forecasted_data)

		plotFile = close_data.join(forecasted_data, how = 'outer')
		plotFile = plotFile.rename(index=str, columns={"Target": "Actual", "yhat_scaled": "Forecasted"})
		plotFile.index.names = ['date']
		plotFile.tail()
		plotFile.to_csv('./app/static/data/predictions/explore/'+str(filename).upper()+'-prediction.csv', na_rep='nan')

		'''
		d = [date, close_data, forecasted_data]
		export_data = izip_longest(*d, fillvalue = '')
		print export_data
		
		
		with open('./app/static/data/predictions/explore/'+str(filename)+'-prediction.csv' , 'wb') as myfile:
			wr = csv.writer(myfile)
			wr.writerow(("Date", "Actual", "Forecasted"))
			wr.writerows(export_data)
		#myfile.close()
		#	print 'save csv'
		'''

		#newFile = Data(name=f.filename, data=f.read(), user_id=current_user.id)
		#db.session.add(newFile)
		#db.session.commit()
		

		return render_template("main/plot_explore.html", original = round(original_end,2), 
								forecast = round(forecast_start,2),
								forecast_future = round(forecast_future,2),
								filename = filename.upper(),
								num_days=num_days, title='forecasting result of ' + filename
								)
	return render_template('main/explore.html', form=form, title='Upload csv')