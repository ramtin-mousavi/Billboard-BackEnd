
from wtforms import Form , BooleanField , StringField , PasswordField , validators , ValidationError


class Register_Form (Form):

    name = StringField ('Name' , [validators.Length (min=3 , max = 50)])
    email = StringField ('Email Address',[validators.Length (min=8 , max = 50) ,validators.Email("لطفا ايميل خود را به درستي وارد کنيد")])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='پسورد ها مطابقت ندارند')])
    confirm = PasswordField ('Please Repeat Password')
    accept_laws = BooleanField('I accept the TOS', [validators.DataRequired()])

    def validate(self):
        if not Form.validate(self):
            return False

        user = User_Model.query.filter_by(email = self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email is already taken")
            return False
        else:
            return True


class Login_Form (Form):

    username = StringField ('Enter Username' , [validators.Length (min=4 , max = 25)])

    password = PasswordField ('Enter Password' , [
        validators.DataRequired()])



class Submit_Form (Form):

    company = StringField ('Company' , [validators.Length (min=3 , max = 50)])
    email = StringField ('Email',[validators.Length (min=8 , max = 50) ,validators.Email("لطفا ايميل خود را به درستي وارد کنيد")])
    phone = StringField ('Phone' , [validators.Length (min=3 , max = 30)])
    name = StringField ('Name' , [validators.Length (min=3 , max = 50)])
    download_link  = StringField ('Download Link' )
    deepLink = StringField ('Deep Link' )
    iconLink = StringField ('Icon Link' )
