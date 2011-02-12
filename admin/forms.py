from flaskext.wtf import Form, TextField, FileField, SelectField, PasswordField
from wtforms.validators import Email, URL, Required

class AuthorForm(Form):
    name = TextField(validators=[Required])
    email = TextField(validators=[Required, Email])

class BannerForm(Form):
    destination = TextField(validators=[Required, URL])
    author_id = SelectField()
    image = FileField()
    
class LoginForm(Form):
    name = TextField(validators=[Required])
    password = PasswordField(validators=[Required])




