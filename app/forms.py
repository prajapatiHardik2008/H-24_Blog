from flask_wtf import FlaskForm
from wtforms  import StringField , PasswordField , SubmitField , BooleanField
from wtforms.validators import DataRequired , Length , Email , EqualTo
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

class LoginForm(FlaskForm):
    email = StringField("UserEmail",validators=[DataRequired(),Email()])
    password = PasswordField("Password",validators=[DataRequired(),Length(min=8 , max= 20)])
    remember = BooleanField("RM")
    submit = SubmitField("Log In ")