from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FloatField, DateField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange, Optional
from app.models import User # For validation against existing users
from datetime import date

class LoginForm(FlaskForm):
    """Form for user login."""
    email = StringField('Email', validators=[DataRequired(message="Email is required."), Email(message="Invalid email address.")])
    password = PasswordField('Password', validators=[DataRequired(message="Password is required.")])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    """Form for user registration."""
    username = StringField('Username', validators=[
        DataRequired(message="Username is required."), 
        Length(min=2, max=64, message="Username must be between 2 and 64 characters.")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Email is required."), 
        Email(message="Invalid email address."), 
        Length(max=120, message="Email must be less than 120 characters.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required."), 
        Length(min=6, message="Password must be at least 6 characters long.")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password."), 
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """Checks if the username is already taken."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    def validate_email(self, email):
        """Checks if the email is already registered."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please use a different one or login.')

class TransactionForm(FlaskForm):
    """Form for adding or editing transactions."""
    type = SelectField('Type', choices=[('income', 'Income'), ('expense', 'Expense')], validators=[DataRequired(message="Please select a transaction type.")])
    category = StringField('Category', validators=[
        DataRequired(message="Category is required."), 
        Length(max=50, message="Category must be less than 50 characters.")
    ])
    amount = FloatField('Amount', validators=[
        DataRequired(message="Amount is required."), 
        NumberRange(min=0.01, message='Amount must be a positive number.')
    ])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired(message="Date is required.")], default=date.today)
    description = TextAreaField('Description (Optional)', validators=[
        Optional(), 
        Length(max=200, message="Description must be less than 200 characters.")
    ])
    submit = SubmitField('Save Transaction')

class SavingsGoalForm(FlaskForm):
    """Form for adding or editing savings goals."""
    name = StringField('Goal Name', validators=[
        DataRequired(message="Goal name is required."), 
        Length(max=100, message="Goal name must be less than 100 characters.")
    ])
    target_amount = FloatField('Target Amount', validators=[
        DataRequired(message="Target amount is required."), 
        NumberRange(min=0.01, message='Target amount must be a positive number.')
    ])
    current_amount = FloatField('Current Amount', validators=[
        DataRequired(message="Current amount is required (can be 0)."), # Default is 0, but still require input if field is shown
        NumberRange(min=0.0, message='Current amount cannot be negative.')
    ], default=0.0)
    deadline = DateField('Deadline (Optional)', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Save Goal')
