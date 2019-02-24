from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextField, IntegerField, DateField, SelectField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.widgets import TextArea
from app.models import User, JobPost, Application

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    # username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

FREQ_TABLE = ('Per Hour','Per Day','Total')


class JobPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    organization = StringField('Organization', validators=[DataRequired()])
    # description = StringField('Job Description', validators=[DataRequired()])
    description = StringField(u'Text', widget=TextArea(),validators=[DataRequired()])
    pay = FloatField('Pay', validators=[DataRequired()])
    pay_frequency = SelectField('Frequency', choices=[(option,option) for option in FREQ_TABLE])
    # start_date = DateField('Date Start',format='%M/%D/%Y')
    # end_date = DateField('Date End',format='%M/%D/%Y')
    submit = SubmitField('Create Listing')

class EditListingForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    organization = StringField('Organization', validators=[DataRequired()])
    # description = StringField('Job Description', validators=[DataRequired()])
    description = StringField(u'Text', widget=TextArea(),validators=[DataRequired()])
    pay = FloatField('Pay', validators=[DataRequired()])
    pay_frequency = SelectField('Frequency', choices=[(option,option) for option in FREQ_TABLE])
    # start_date = DateField('Date Start',format='%M/%D/%Y')
    # end_date = DateField('Date End',format='%M/%D/%Y')
    submit = SubmitField('Save Listing')

class DeleteListingBtn(FlaskForm):
    submit = SubmitField('Delete Listing')

class ApplyJobBtn(FlaskForm):
    submit = SubmitField('Apply')


SEX_TABLE = ('','Male','Female')

class EditProfileForm(FlaskForm):
    gender = SelectField('Gender', choices=[(option,option) for option in SEX_TABLE])
    bio = StringField(u'Text', widget=TextArea())
    phone_no = IntegerField('Phone Number')
    submit = SubmitField('Save Profile')

class AcceptApplicationBtn(FlaskForm):
    submit = SubmitField('Accept')

class RejectApplicationBtn(FlaskForm):
    submit = SubmitField('Reject')
