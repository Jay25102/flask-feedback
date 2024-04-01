from flask import Flask, flash, redirect, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized
from models import *
from forms import *
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flaskfeedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "somekey"
toolbar = DebugToolbarExtension(app)

bcrypt = Bcrypt()

connect_db(app)
db.create_all()

@app.route("/")
def root():
    """redirects to /register"""

    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def registration_page():
    """handles the form and submission for registration of a new user"""

    form = RegisterNewUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)

        db.session.commit()
        session['username'] = user.username
        
        return redirect(f"/users/{username}")
    
    else:
        return render_template("register_new_user_form.html", form=form)
    
@app.route("/login", methods=["GET", "POST"])
def login_page():
    """handles login form and authentication"""

    form = LoginExistingUser()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect(f"/users/{username}")
        
        else:
            form.username.errors = ["Incorrect username/password"]

    return render_template("login_user_form.html", form=form)


@app.route("/users/<username>")
def display_user_info(username):
    """secret info page for logged in users"""

    if "username" not in session:
        flash("You must be logged in to view this page")
        return redirect("/login")
    
    user = User.query.get(username)

    return render_template("user_info.html", user=user)

@app.route("/logout")
def logout():
    """logs the current user out of the session"""
    session.pop("username")
    
    return redirect("/login")

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """deletes user once verified"""

    if "username" not in session or username != session["username"]:
        raise Unauthorized()
    
    user = User.query.get(username)

    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/register")

@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_new_feedback(username):
    """handles adding new feedback to db"""

    if "username" not in session or username != session["username"]:
        raise Unauthorized()

    form = AddNewFeedback()

    if form.validate_on_submit():

        title = form.title.data
        content = form.content.data

        newFeedback = Feedback(title=title,
                               content=content,
                               username=username)
        db.session.add(newFeedback)
        db.session.commit()

        return redirect(f"/users/{username}")
    else:
        return render_template("new_feedback.html", form=form)
    
@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """handles updating existing feedback"""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session["username"]:
        raise Unauthorized()
    
    form = AddNewFeedback(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")
    
    return render_template("/edit_feedback.html", form=form, feedback=feedback)

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """deletes feedback from db"""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session["username"]:
        raise Unauthorized()
    
    db.session.delete(feedback)
    db.session.commit()

    return redirect(f"/users/{feedback.username}")