import sys
sys.path.append("..")

from Models import Model
from flask_login import current_user

class Load_User:

    @staticmethod
    @login_manager.user_loader
    def load_user(userid):
        return Model.User_Model.query.get(int(userid))



class Main :

    @staticmethod
    def home_page():
        if current_user.is_authenticated:
            return redirect (url_for('profile_handler' , page_numb = 1))

        return render_template('main.html')



class Sign_Up :

    @staticmethod
    def sign_up ():


        register_form = Register_Form (request.form)

        if register_form.validate ():
            if request.method == 'POST' :

                user = User_Model (request.form['name'] , request.form['email'] , request.form['password'])
                user.add_and_commit ()

                flash ('شما با موفقيت ثبت نام شديد')
                flash ('لطفا از منوي «ورود» اقدام به وارد شدن فرماييد')

                return redirect (url_for('home_page'))

            else:
                return redirect (url_for('home_page'))


        if 'name' in register_form.errors:
            flash ('لطفا فيلد نام و نام خانوادگي را پر کنيد')
        if 'email' in register_form.errors:
            flash ('لطفا فيلد ايميل را پر کنيد')
        if 'password' in register_form.errors  :
            flash ('لطفا فيلدهاي پسورد را به درستي وارد کنيد')
        if 'accept_laws' in register_form.errors:
            flash ('شما بايد با قوانين بيلبورد موافقت کنيد')


        return redirect (url_for ('home_page'))



class Login :

    @staticmethod
    def login():

        login_form = Login_Form (request.form)

        if request.method == 'POST' and login_form.validate():
            if login_form.validate():

                stored_user = User_Model.email_query (request.form['username'])

                if (stored_user is not None) and (stored_user.check_password(request.form['password'])):
                    login_user(stored_user)

                    if stored_user.email == 'admin':

                        return redirect (url_for ('admin_panel'))

                    return redirect (url_for('profile_handler' , page_numb = 1))
                    
                else:
                    if stored_user is None:
                        flash ('لطفا ايميل خود را به درستي وارد کنيد و يا از منوي ثبت نام اقدام به ثبت نام فرماييد')

                    elif not stored_user.check_password(request.form['password']):
                        flash ('لطفا پسورد خود را به درستي وارد کنيد')

                    return redirect (url_for('home_page'))

            flash ("لطفا اطلاعات ورود را به درستي وارد کنيد")
            return redirect (url_for('home_page'))
        return redirect (url_for('home_page'))
