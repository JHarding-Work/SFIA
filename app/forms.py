from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired,Length,ValidationError
class Login_Form(FlaskForm):
    username = StringField('Username')
    password = StringField('Password')
    submit = SubmitField('Sign in')

class Sign_Up_Form(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=6,max=20)])
    password = StringField('Password',validators=[DataRequired(),Length(min=8)])
    submit = SubmitField('Sign up')
    
    ##### Fix this Later #####
    def validate_password(self, password):
            
            special_char = ['!','£','$','%','^','&','*','(',')',';',':']
            digits = list(i for i in range(0,10))
        
            for i in special_char:
                if not(i in password.data):
                    raise ValidationError(f"Password must include one special character from {special_char}")
    
            for i in digits:
                if not(digits in password.data):
                    raise ValidationError("Password must include at least one number")

