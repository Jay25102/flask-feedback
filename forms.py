from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
# highlighed as not being used, but is required otherwise flask throws an error
# Exception: Install 'email_validator' for email validation support.
import email_validator

class RegisterNewUserForm(FlaskForm):
    """form for registering a new user"""

    username = StringField("username", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])
    email = EmailField("email", validators=[Email(), InputRequired()])
    first_name = StringField("first_name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("last_name", validators=[InputRequired(), Length(max=30)])

class LoginExistingUser(FlaskForm):
    """form for logging in a user"""

    username = StringField("username", validators=[InputRequired()])
    password = PasswordField("password", validators=[InputRequired()])

class AddNewFeedback(FlaskForm):
    """form for new user feedback"""

    title = StringField("title", validators=[InputRequired(), Length(max=100)])
    content = StringField("content", validators=[InputRequired()])