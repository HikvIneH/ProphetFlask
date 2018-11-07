from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, NumberRange

class DashboardForm(FlaskForm):
    stock = StringField('Stock Symbol', validators=[DataRequired()])
    num_days_back = IntegerField('Number of days back', validators=[DataRequired(message='Must be Integer!'), NumberRange(min=365, message='Assign to more than 365')])
    num_days_ahead = IntegerField('Number of days to predict', validators=[DataRequired(message='Must be Integer!'), NumberRange(min=1, message='Assign to more than a day')])
    #submit = SubmitField('Submit')

    '''
    def validate_data(self, form, field):
        if not field.data or isinstance(field.data, string_types) and not field.data.strip():
            raise ValidationError('The more the better, raise the value to more than a year')
    '''