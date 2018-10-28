

from Models import Model
from flask_login import login_required, login_user, logout_user , LoginManager, current_user
from flask import Flask, flash, redirect, render_template, request, url_for , make_response
from flask_sqlalchemy import SQLAlchemy
import os
from Forms import Forms


app = Flask(__name__ , static_folder = 'statics' , template_folder = 'Views')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Ramtin/Desktop/BillBoard Project/DataBase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DataBase = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.init_app(app)
login_manager.login_view = 'login'


class Load_User:

    @staticmethod
    @login_manager.user_loader
    def load_user(userid):
        return Model.User_Model.query.get(int(userid))



class Home :

    @staticmethod
    def home_page():

        if current_user.is_authenticated:
            return redirect (url_for('show_apps' , page_numb = 1))

        return render_template('main.html')



class Sign_Up :

    @staticmethod
    def sign_up ():


        register_form = Forms.Register_Form (request.form)

        if register_form.validate ():
            if request.method == 'POST' :

                user = Model.User_Model (request.form['name'] , request.form['email'] , request.form['password'])
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

        login_form = Forms.Login_Form (request.form)

        if request.method == 'POST' and login_form.validate():
            if login_form.validate():

                stored_user = Model.User_Model.email_query (request.form['username'])

                if (stored_user is not None) and (stored_user.check_password(request.form['password'])):
                    login_user(stored_user)

                    if stored_user.email == 'admin':
                        return redirect (url_for ('render_admin_panel'))

                    return redirect (url_for('show_apps' , page_numb = 1))

                else:
                    if stored_user is None:
                        flash ('لطفا ايميل خود را به درستي وارد کنيد و يا از منوي ثبت نام اقدام به ثبت نام فرماييد')

                    elif not stored_user.check_password(request.form['password']):
                        flash ('لطفا پسورد خود را به درستي وارد کنيد')

                    return redirect (url_for('home_page'))

            flash ("لطفا اطلاعات ورود را به درستي وارد کنيد")
            return redirect (url_for('home_page'))
        return redirect (url_for('home_page'))




class Logout:

    @staticmethod
    def logout ():

        if not current_user.is_authenticated:
            return redirect (url_for('home_page'))

        logout_user()
        flash('با موفقيت خارج شديد. به اميد ديدار مجدد')
        return render_template('main.html')





class Show_Apps_Manager:

    @staticmethod
    @login_required
    def show_apps (page_numb):

        req = request.form.get ('option')

        #If User Select An Option
        if req != None:

            if int (req) == 3:
                apps = Model.Android_Model.paginate_by_filter (8,page_numb,True,'Game')
                return render_template ('profile.html', user = Load_User.load_user (current_user.id) , apps = apps)

            elif int (req) == 2:
                apps = Model.Android_Model.paginate_by_filter (8,page_numb,True,'App')
                return render_template ('profile.html', user = Load_User.load_user (current_user.id) , apps = apps)

            elif int ( req ) == 1:
                apps = Model.Android_Model.paginate_query (8,page_numb,True)
                return render_template ('profile.html', user = Load_User.load_user (current_user.id) , apps = apps)

        # If No Filter
        else:
            apps = Model.Android_Model.paginate_query (8,page_numb,True)
            return render_template ('profile.html', user = Load_User.load_user (current_user.id) , apps = apps)


class Show_Gifts_Manager:

    @staticmethod
    @login_required
    def show_gifts (page_numb):

        gifts = Model.Gift_Model.paginate_query (8, page_numb, True)
        return render_template ('giftshop.html' ,user = Load_User.load_user (current_user.id) , gifts = gifts)




class Shopping_Handler:

    @staticmethod
    @login_required
    def buy_gift (id):

        temp_gift = Model.Gift_Model.id_query (id)

        if temp_gift.supply > 0:
            user = Load_User.load_user (current_user.id)

            if user.credit > temp_gift.cost:



                user.discharge (temp_gift.cost)
                temp_gift.discharge()


                #Save Transaction Record
                gift_history = Model.Gift_History_Model (user.id , temp_gift.id)
                gift_history.add_and_commit()

                return render_template ('giftresult.html' , gift = temp_gift)

            flash ('اعتبار شما کافي نيست')
            return redirect (url_for('show_apps' , page_numb = 1))

        return "In Gift Tamum Shode!"


class Advertising :

    @staticmethod
    @login_required
    def request_new_ad ():

        return render_template ('submitAd.html')


    @staticmethod
    @login_required
    def submit_new_ad ():

        submit_form = Forms.Submit_Form (request.form)

        if submit_form.validate ():
            if request.method == 'POST' :

                new_app = Model.Android_Model (request.form ['name'] , request.form ['iconlink'] , 'App' , 100 , request.form ['dllink'] , request.form ['deeplink'] ,
                                       request.form ['company'] , request.form ['email'] , request.form ['phone'] )
                new_app.add_and_commit ()
                flash ('آگهي شما ثبت شد و پس از تاييد در سايت قرار داده خواهد شد')

                return redirect (url_for ('show_apps' , page_numb = 1))

            #if GET
            return redirect (url_for ('request_new_ad'))

        #if Not Valid Form
        flash ('لطفا اطلاعات را به درستي وارد نماييد')
        return redirect (url_for('request_new_ad'))


class Admin_Panel:

    @staticmethod
    @login_required
    def render_admin_panel ():

        if Load_User.load_user (current_user.id).email == 'admin':
            return render_template ('adminDashboard.html')

        return "Access Denied"



class Approve_System:

    @staticmethod
    @login_required
    def get_pending_requests(page_numb):

        if Load_User.load_user (current_user.id).email == 'admin':

            apps = Model.Android_Model.paginate_query_for_admin (8 , page_numb , True)
            return render_template ('adminPendingRequests.html' , apps = apps)


        return "Access Denied"


    @staticmethod
    @login_required
    def approve_or_reject (id):

        app = Model.Android_Model.query.get (id)
        if request.form ['submit'] == 'approve':

            app.approve()
            flash ('با موفقيت تاييد شد')
            return redirect (url_for ('get_pending_requests' , page_numb = 1))


        elif request.form ['submit'] == 'reject':

            app.reject()
            flash ('با موفقيت رد شد')
            return redirect (url_for ('get_pending_requests' , page_numb = 1))


        else:
            return redirect (url_for ('get_pending_requests' , page_numb = 1))



class Gift_History_Manager:

    @staticmethod
    @login_required
    def gift_history_handler(page_numb):

        user = Load_User.load_user (current_user.id)
        user_id = user.id
        history = Model.Gift_History_Model.paginate_query(8, page_numb, True, user_id)

        return render_template('NewHistory.html', history = history , user = user)


class Survey_Manager:

    @staticmethod
    @login_required
    def add_survey ():

        return render_template ('temp.html')


    @staticmethod
    @login_required
    def get_survey ():

        count = request.form ['questions_count']
        survey = Model.Survey_Model (request.form ['question_name'] , 'description')
        survey.add_and_commit()

        for question_number in range (int(count)):

            new_question = Model.Question_Model (request.form ['q'+str(question_number)] , survey.id)
            new_question.add_and_commit()

            for item in request.form.getlist('item'+str(question_number)):

                new_item = Model.Item_Model (item , new_question.id)
                new_item.add_and_commit()


        return "DONE"

#URLs
app.add_url_rule('/' , view_func = Home.home_page)
app.add_url_rule('/signUp' , view_func = Sign_Up.sign_up , methods = ['POST' , 'GET'])
app.add_url_rule('/login' , view_func = Login.login , methods = ['POST' , 'GET'])
app.add_url_rule('/logout' , view_func = Logout.logout)
app.add_url_rule('/profile/<int:page_numb>/' , view_func = Show_Apps_Manager.show_apps, methods = ['POST' , 'GET'])
app.add_url_rule('/giftshop/<int:page_numb>/' , view_func = Show_Gifts_Manager.show_gifts )
app.add_url_rule('/shoppingresult/<int:id>/' , view_func = Shopping_Handler.buy_gift , methods = ['POST' , 'GET'])
app.add_url_rule('/addad',view_func=Advertising.request_new_ad)
app.add_url_rule('/submitadd' , view_func = Advertising.submit_new_ad , methods = ['POST' , 'GET'])
app.add_url_rule('/adminpanel' , view_func = Admin_Panel.render_admin_panel)
app.add_url_rule('/getPendingRequests/<int:page_numb>' , view_func = Approve_System.get_pending_requests)
app.add_url_rule('/approveorreject/<int:id>' , view_func = Approve_System.approve_or_reject , methods = ['POST' , 'GET'])
    #app.add_url_rule('/addhistory' , view_func = Download_History_Manager.add_history , methods = ['POST' , 'GET'])
    #app.add_url_rule('/getconfirminstalllist/<int:page_numb>' , view_func = Download_History_Manager.get_confirm_install_list )
    #app.add_url_rule('/addcredit' , view_func = Credit_Manager.add_credit , methods = ['POST' , 'GET'])
    #app.add_url_rule('/revertactions/<appName>' , view_func = Credit_Manager.revert_actions)
app.add_url_rule('/gifthistory/<int:page_numb>/' , view_func = Gift_History_Manager.gift_history_handler)
app.add_url_rule('/addSurvey' , view_func = Survey_Manager.add_survey)
app.add_url_rule('/getSurvey' , view_func = Survey_Manager.get_survey , methods = ['GET','POST'])




if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run ()
    #app.run(host = '192.168.1.108' , port = 5000, debug = False)

# Correct Names
#Correct Survey_Manager
