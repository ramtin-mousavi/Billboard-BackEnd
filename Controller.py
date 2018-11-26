

from Models import Model
from flask_login import login_required, login_user, logout_user , LoginManager, current_user
from flask import Flask, flash, redirect, render_template, request, url_for , make_response, jsonify , session
from flask_sqlalchemy import SQLAlchemy
import os
from Forms import Forms
from flask_marshmallow import Marshmallow
import os



app = Flask(__name__ , static_folder = 'statics' , template_folder = 'Views')

dir_path = os.path.dirname(os.path.realpath(__file__)).replace ("\\" , '/').split(':')[1]
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+dir_path+'/DataBase.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DataBase = SQLAlchemy(app)
MarshMallow = Marshmallow (app)


login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.init_app(app)
login_manager.login_view = 'login'


class Load_User:

    @staticmethod
    @login_manager.user_loader
    def load_user(userid):
        return Model.User_Model.query.get(int(userid))



class Sign_Up :

    @app.route('/api/signup', methods=["POST"])

    def sign_up():

        if request.method == 'POST':

            req = request.get_json()

            name = req["name"]
            email = req["email"]
            password = req["password"]

            new_user = Model.User_Model(name, email, password)
            new_user.add_and_commit()

            return jsonify(Model.user_model_schema.dump (new_user).data)

        else:
            return "method is not POST"

app.add_url_rule('/signup' , view_func = Sign_Up.sign_up , methods = ['POST' , 'GET'])


class Login :

    def login():


        if request.method == 'POST' :

            req = request.get_json()

            username = req["username"]
            password = req["password"]

            stored_user = Model.User_Model.email_query (username)

            if (stored_user is not None) and (stored_user.check_password(password)):

                login_user (stored_user)
                session ['user_id'] = stored_user.id

                if stored_user.email == 'admin':
                    session ['role'] = 'user'
                else:
                    session ['role'] = 'admin'

                return jsonify(Model.user_model_schema.dump (stored_user).data)


            else:
                if stored_user is None:
                    return "user is not found or entered email is wrong."

                elif not stored_user.check_password(req['password']):
                    return "password is incorrect."

        else:
            return "request is not post"


app.add_url_rule('/api/login' , view_func = Login.login , methods = ['POST' , 'GET'])


class Logout:

    @staticmethod
    def logout ():

        if not current_user.is_authenticated:
            return "you have not logged in"

        logout_user()
        session.pop ('user_id', None)
        session.pop ('role', None)

        return jsonify (Model.user_model_schema.dump (current_user).data)

app.add_url_rule('/api/logout' , view_func = Logout.logout)




class Show_Apps_Manager:

    @staticmethod
    @login_required
    def show_apps ():

        req = int (request.get_json()['option'])

        if int (req) == 3:
            apps = Model.Android_Model.filter_query ('Game')
            out = Model.androids_model_schema.dump (apps).data
            return jsonify (out)

        elif int (req) == 2:
            apps = Model.Android_Model.filter_query ('App')
            out = Model.androids_model_schema.dump (apps).data
            return jsonify (out)

        elif int ( req ) == 1:
            apps = Model.Android_Model.all_query()
            out = Model.androids_model_schema.dump (apps).data
            return jsonify (out)


app.add_url_rule('/api/profile' , view_func = Show_Apps_Manager.show_apps, methods = ['POST' , 'GET'])



class Show_Gifts_Manager:

    @staticmethod
    @login_required
    def show_gifts ():

        gifts = Model.Gift_Model.query.filter(Model.Gift_Model.supply > 0)
        out = Model.gifts_model_schema.dump (gifts).data
        return jsonify (out)

app.add_url_rule('/api/giftshop' , view_func = Show_Gifts_Manager.show_gifts )




class Shopping_Handler:

    @staticmethod
    @login_required
    def buy_gift ():

        temp_gift = Model.Gift_Model.query.get (request.get_json()['gift_id'])

        if temp_gift.supply > 0:

            user = Model.User_Model.query.get (session['user_id'])

            if user.credit > temp_gift.cost:

                user.discharge (temp_gift.cost)
                temp_gift.discharge()


                #Save Transaction Record
                gift_history = Model.Gift_History_Model (user.id , temp_gift.id)
                gift_history.add_and_commit()

                return jsonify (Model.gift_history_schema.dump (gift_history).data)

            return "not enough credit"

        return "gift has been finished"

app.add_url_rule('/api/shoppingresult' , view_func = Shopping_Handler.buy_gift , methods = ['POST' , 'GET'])


'''
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
'''



class Approve_System:

    @staticmethod
    @login_required
    def get_pending_requests():

        if session ['role'] == 'admin':

            apps = Model.Android_Model.query_for_admin()
            out = Model.androids_model_schema.dump (apps).data
            return jsonify (out)


        return "Access Denied"


    @staticmethod
    @login_required
    def approve_or_reject (id):

        if request.method == 'POST':

            req = request.get_json()

            app = Model.Android_Model.query.get (int (req['app_id']))

            if req ['submit'] == 'approve':

                app.approve()
                return "approved successfully"


            elif req ['submit'] == 'reject':

                app.reject()
                return "rejected successfully"


        return "request is not post"


app.add_url_rule('/api/getPendingRequests' , view_func = Approve_System.get_pending_requests)
app.add_url_rule('/api/approveorreject' , view_func = Approve_System.approve_or_reject , methods = ['POST' , 'GET'])



class Gift_History_Manager:

    @staticmethod
    @login_required
    def gift_history_handler():

        user_id = session ['user_id']
        histories = Model.Gift_History_Model.query.filter_by (user_id = user_id)
        output = Model.gifts_history_schema.dump (histories).data
        return jsonify (output)

app.add_url_rule('/api/gifthistory/' , view_func = Gift_History_Manager.gift_history_handler)


class Survey_Manager:

    @staticmethod
    @login_required
    def get_survey ():

        req = request.get_json()

        pass

'''
        count = request.form ['questions_count']
        survey = Model.Survey_Model (request.form ['question_name'] , 'description')
        survey.add_and_commit()

        for question_number in range (int(count)):

            new_question = Model.Question_Model (request.form ['q'+str(question_number)] , survey.id)
            new_question.add_and_commit()

            for item in request.form.getlist('item'+str(question_number)):

                new_item = Model.Item_Model (item , new_question.id)
                new_item.add_and_commit()

        flash ('فرم نظر سنجی شما با موفقیت دریافت شد')
        return redirect (url_for("show_apps" , page_numb = 1))'''

app.add_url_rule('/api/getSurvey' , view_func = Survey_Manager.get_survey , methods = ['GET','POST'])



@login_required
def show_survey():

    surveys = Model.Survey_Model.query.all()
    output = Model.surveys_schema.dump (surveys).data

    return jsonify (output)

app.add_url_rule('/api/showSurvey' , view_func = show_survey )


@login_required
def fill_survey (id):

    survey = Model.Survey_Model.query.get (id)
    output = Model.survey_schema.dump (survey).data

    return jsonify (output)

app.add_url_rule('/api/fillSurvey/<int:id>' , view_func = fill_survey )


@login_required
def submit_filling():
    req = request.get_json()
    for key  in req
        item = Model.Item_Model.query.get (int(req[key]))
        item.vote()

    return "voted successfully"

app.add_url_rule('/api/submitFilling' , view_func = submit_filling , methods = ['GET','POST'])




#URLs
    #app.add_url_rule('/addad',view_func=Advertising.request_new_ad)
    #app.add_url_rule('/submitadd' , view_func = Advertising.submit_new_ad , methods = ['POST' , 'GET'])
    #app.add_url_rule('/addhistory' , view_func = Download_History_Manager.add_history , methods = ['POST' , 'GET'])
    #app.add_url_rule('/getconfirminstalllist/<int:page_numb>' , view_func = Download_History_Manager.get_confirm_install_list )
    #app.add_url_rule('/addcredit' , view_func = Credit_Manager.add_credit , methods = ['POST' , 'GET'])
    #app.add_url_rule('/revertactions/<appName>' , view_func = Credit_Manager.revert_actions)











if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run (debug = True)
    #app.run(host = '192.168.1.108' , port = 5000, debug = False)

# Correct Names
#Correct Survey_Manager
