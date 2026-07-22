from flask_wtf import FlaskForm
from wtforms  import StringField , PasswordField , SubmitField , BooleanField
from wtforms.validators import DataRequired , Length , Email , EqualTo , ValidationError
from app.models import User
from app import login_manager

@login_manager.user_loader
def load_user(user_id):
     return User.query.get(int(user_id))


class registration(FlaskForm):   # it is inher. Flask form 
    username = StringField("UserName",validators=[DataRequired(),Length(min=2,max=10) ]) # data is requried and min length is 2 or max len os 10 
    email = StringField("Useremail",validators=[DataRequired(),Email()]) 
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, max=20)
        ]
    )

    Confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            Length(min=8, max=20),
            EqualTo("password", message="Passwords must match")
        ]
    )    
    submit = SubmitField("Sign Up")

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user :
            raise ValidationError(" Username is already taken. ")
    def validate_email(self,email):
            email = User.query.filter_by(email=email.data).first()
            if email :
                raise ValidationError("Email is already taken ")

class LoginForm(FlaskForm):
    email = StringField("UserEmail",validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired(),Length(min=8 , max= 20)])
    remember = BooleanField("RM")
    submit = SubmitField("Log In ")