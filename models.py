from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    app.app_context().push()
    db.app = app
    db.init_app(app)

class User(db.Model):
    """model for user including info and register/authentication functions"""

    __tablename__ = "users"

    username = db.Column(db.Text,
                         primary_key=True,
                         unique=True,
                         nullable=False)
    password = db.Column(db.Text,
                         nullable=False)
    email = db.Column(db.String(50),
                      nullable=False,
                      unique=True)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                          nullable=False)
    
    feedback = db.relationship("Feedback", backref="user", cascade="all,delete")
    
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """uses bcrypt to register a new user to db"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        newUser = cls(username=username,
                      password=hashed_utf8,
                      email=email,
                      first_name=first_name,
                      last_name=last_name)
        db.session.add(newUser)

        return newUser
    
    @classmethod
    def authenticate(cls, username, password):
        """authenticates user for login"""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False
        

class Feedback(db.Model):
    """model for user feedback"""

    __tablename__ = "feedback"

    id = db.Column(db.Integer,
                   primary_key=True)
    title = db.Column(db.String(100),
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    username = db.Column(db.Text(),
                         db.ForeignKey('users.username'),
                         nullable=False)
    
