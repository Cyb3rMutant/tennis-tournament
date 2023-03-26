from wtforms import Form, BooleanField, StringField, PasswordField, validators


class RegistrationForm(Form):
    name = StringField('name', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [validators.DataRequired()])
    confirm = PasswordField('Repeat Password', [validators.DataRequired(), validators.EqualTo('password', message='Passwords must match')])
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])


class LoginForm(Form):
    email = StringField('Email Address', [validators.InputRequired(), validators.Length(min=6, max=35)], render_kw={"placeholder": "Email Address"})
    password = PasswordField('Password', render_kw={"placeholder": "Password"})

