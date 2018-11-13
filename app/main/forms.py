from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed

from wtforms import IntegerField, StringField, SubmitField, ValidationError, BooleanField
from wtforms.validators import DataRequired, NumberRange
from wtforms.fields.html5 import IntegerRangeField

class DashboardForm(FlaskForm):
	stock = StringField('Stock Symbol (E.g. AAPL, TSLA, ^GSPC)', validators=[DataRequired()])
	'''
	num_days_ahead = IntegerRangeField('Forecast days', default=1)
	num_days_back = IntegerRangeField('Historical range days', default=365)
	'''
	num_days_back = IntegerField('Number of days back (n > 365)', 
		validators=[DataRequired(message='Must be Integer!'), 
		NumberRange(min=365, 
		message='Assign to more than 365')
		])
		
	num_days_ahead = IntegerField('Number of days to predict', 
		validators=[DataRequired(message='Must be Integer!'), 
		NumberRange(min=1, 
		message='Assign to more than a day')
		])
	#submit = SubmitField(label="Process")
	
	'''
	def validate_data(self, form, field):
		if not field.data or isinstance(field.data, string_types) and not field.data.strip():
			raise ValidationError('The more the better, raise the value to more than a year')
	'''

class UploadForm(FlaskForm):
	data = FileField('', validators=[
		FileRequired(),
		FileAllowed(['csv'], '.csv only!')
		])
	'''
	num_days_ahead = IntegerField('Days ahead', validators=[DataRequired(message='Must be Integer!'), 
		NumberRange(min=1, 
		message='Assign to more than a day')
		])
	'''
	num_days_ahead = IntegerRangeField('Forecast days', default=1)
	dailySeasonality = BooleanField('daily')
	weeklySeasonality = BooleanField('weekly')
	yearlySeasonality = BooleanField('yearly')
	#submit = SubmitField(label="Process")

