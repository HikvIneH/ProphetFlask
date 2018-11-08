from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, NumberRange

class DashboardForm(FlaskForm):
    stock = StringField('Enter stock Symbol (E.g. AAPL, MSFT, TSLA, ^GSPC)', validators=[DataRequired()])
    num_days_back = IntegerField('Enter number of days back (n > 365)', validators=[DataRequired(message='Must be Integer!'), NumberRange(min=365, message='Assign to more than 365')])
    num_days_ahead = IntegerField('Enter number of days to predict', validators=[DataRequired(message='Must be Integer!'), NumberRange(min=1, message='Assign to more than a day')])

    '''
    def validate_data(self, form, field):
        if not field.data or isinstance(field.data, string_types) and not field.data.strip():
            raise ValidationError('The more the better, raise the value to more than a year')
    '''