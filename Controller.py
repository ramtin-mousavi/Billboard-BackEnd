

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






class Sign_Up :

    def sign_up():

        if request.method == 'POST':

            req = request.get_json()

            name = req["name"]
            email = req["email"]
            password = req["password"]

            new_user = Model.User_Model(name, email, password)
            new_user.add_and_commit()

            out = {'user':new_user.serialize_one() , 'status':'OK'}
            return jsonify(out)

<<<<<<< HEAD
||||||| merged common ancestors
    @app.route('/api/v1/signup', methods=["POST"])
    def sign_up_api():
        register_form = Forms.Register_Form(request.form)
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        if register_form.validate():
            if request.method == 'POST':
                user = Model.User_Model(name, email, password)
                user.add_and_commit()
                return jsonify(user.serialize())
            else:
                return "method is not POST."
=======
    @app.route('/api/v1/signup', methods=["POST"])
    def sign_up_api():
        register_req = request.get_json()
        name = register_req.get("name")
        email = register_req.get("email")
        password = register_req.get("password")
        confirm = register_req.get("confirm")
        accept_laws = register_req.get("accept_laws")
        error = None
        if register_req is None:
            return 'request body can not be empty!'
        if name is None:
            error = 'username field cannot be empty!'
        else:
            x = Model.User_Model.query.filter_by(name=register_req.get("name")).first()
            if x is not None:
                error = 'user with this email already exists!'
        if password is None:
            error = 'password field cannot be empty!'
        else:
            if not (confirm == password):
                error = "passwords does not match"
        if accept_laws == 'false':
            error = 'laws should be accepted.'
        if error is None:
            user = Model.User_Model(name, email, password)
            user.add_and_commit()
            return jsonify(user.serialize())
>>>>>>> 086857b1e45e94e30f6e3a3698cef238bc42a2cd
        else:
<<<<<<< HEAD
            out = {'user':'', 'status':"method is not POST"}
            return jsonify (out)
||||||| merged common ancestors
            if 'name' in register_form.errors:
                return jsonify(register_form.errors['name'])
            if 'email' in register_form.errors:
                return jsonify(register_form.errors['email'])
            if "password" in register_form.errors:
                return jsonify(register_form.errors['password'])
            if 'accept_laws' in register_form.errors:
                jsonify(register_form.errors['accept_laws'])
=======
            return jsonify(error)
>>>>>>> 086857b1e45e94e30f6e3a3698cef238bc42a2cd

app.add_url_rule('/api/signup' , view_func = Sign_Up.sign_up , methods = ['POST' , 'GET'])


class Login :

    def login():


        if request.method == 'POST' :

            req = request.get_json()

            email = req["email"]
            password = req["password"]

            stored_user = Model.User_Model.email_query (email)

            if (stored_user is not None) and (stored_user.check_password(password)):

                login_user (stored_user)
                session ['user_id'] = stored_user.id

<<<<<<< HEAD
                if stored_user.email == 'admin':
                    session ['role'] = 'admin'
                    out = {'user':stored_user.serialize_one() , 'role':'admin', 'status':'OK'}
                else:
                    session ['role'] = 'user'
                    out = {'user':stored_user.serialize_one() , 'role':'user', 'status':'OK'}
||||||| merged common ancestors
    @app.route('/api/v1/login', methods=["POST"])
    def login_api():
        login_form = Forms.Login_Form (request.form)
        username = request.form["username"]
        password = request.form["password"]
        if request.method == 'POST' and login_form.validate():
            if login_form.validate():
                stored_user = Model.User_Model.email_query (username)
                if (stored_user is not None) and (stored_user.check_password(password)):
                    return jsonify(stored_user.serialize())
                else:
                    if stored_user is None:
                        return "user is not found or entered email is wrong."
                    elif not stored_user.check_password(request.form['password']):
                        return "password is incorrect."
        else:
            return "form is not valid or method is not POST."

    @staticmethod
    def login():

        login_form = Forms.Login_Form (request.form)

        if request.method == 'POST' and login_form.validate():
            if login_form.validate():

                stored_user = Model.User_Model.email_query (request.form['username'])
=======
    @app.route('/api/v1/login', methods=["POST"])
    def login_api():
        register_req = request.get_json()
        username = register_req.get("username")
        password = register_req.get("password")
        error = None
        if register_req is None:
            return 'request body can not be empty!'
        if username is None:
            error = 'username field cannot be empty!'
        if password is None:
            error = 'password field cannot be empty!'
        if error is None:
            stored_user = Model.User_Model.email_query(username)
            if (stored_user is not None) and (stored_user.check_password(password)):
                return jsonify(stored_user.serialize())
            else:
                if stored_user is None:
                    return "user is not found or entered email is wrong."
                elif not stored_user.check_password(request.form['password']):
                    return "password is incorrect."
        else:
            return jsonify(error)

    @staticmethod
    def login():

        login_form = Forms.Login_Form (request.form)

        if request.method == 'POST' and login_form.validate():
            if login_form.validate():

                stored_user = Model.User_Model.email_query (request.form['username'])
>>>>>>> 086857b1e45e94e30f6e3a3698cef238bc42a2cd

                return jsonify(out)


            else:
                if stored_user is None:
                    out = {'user':'', 'role':'', 'status':'user not found'}
                    return jsonify (out)

                elif not stored_user.check_password(req['password']):
                    out = {'user':'' , 'role':'', 'status':'password incorrect'}
                    return jsonify (out)

        else:
            out = {'user':'','role':'','status':'method is not POST'}
            return jsonify (out)


app.add_url_rule('/api/login' , view_func = Login.login , methods = ['POST' , 'GET'])


class Logout:

    @staticmethod
    def logout ():

        if not current_user.is_authenticated:
            return "you have not logged in"

        logout_user()
        session.pop ('user_id', None)
        role = session.pop ('role', None)

        out = {'user':Model.user_model_schema.dump (current_user).data , 'role':role, 'status':'OK'}
        return jsonify (out)

app.add_url_rule('/api/logout' , view_func = Logout.logout)




class Show_Apps_Manager:

    @staticmethod
    @login_required
    def show_apps (filter=None):

        if filter:
            if int (filter) == 3:
                apps = Model.Android_Model.filter_query ('Game')
                out = {'apps':Model.Android_Model.serialize_many (apps) , 'status': 'OK'}
                return jsonify (out)

            elif int (filter) == 2:
                apps = Model.Android_Model.filter_query ('App')
                out = {'apps':Model.Android_Model.serialize_many (apps) , 'status': 'OK'}
                return jsonify (out)

            elif int (filter) == 1:
                apps = Model.Android_Model.all_query()
                out = {'apps':Model.Android_Model.serialize_many (apps) , 'status': 'OK'}
                return jsonify (out)


        apps = Model.Android_Model.all_query()
        out = {'apps':Model.Android_Model.serialize_many (apps) , 'status': 'OK'}
        return jsonify (out)


app.add_url_rule('/api/showApps/<int:filter>' , view_func = Show_Apps_Manager.show_apps)
app.add_url_rule('/api/showApps/' , view_func = Show_Apps_Manager.show_apps)



class Show_Gifts_Manager:

    @staticmethod
    @login_required
    def show_gifts ():

        gifts = Model.Gift_Model.query.filter(Model.Gift_Model.supply > 0)
        out = {'gifts':Model.Gift_Model.serialize_many(gifts), 'status':'OK'}
        return jsonify (out)

app.add_url_rule('/api/giftshop' , view_func = Show_Gifts_Manager.show_gifts )




class Shopping_Handler:

    @staticmethod
    @login_required
    def buy_gift (gift_id):

        temp_gift = Model.Gift_Model.query.get (int(gift_id))
        if temp_gift:
            if temp_gift.supply > 0:

                user = Model.User_Model.query.get (session['user_id'])

                if user.credit > temp_gift.cost:

                    user.discharge (temp_gift.cost)
                    temp_gift.discharge()

                    #Save Transaction Record
                    gift_history = Model.Gift_History_Model (user.id , temp_gift.id)
                    gift_history.add_and_commit()

                    out = {'user':user.serialize_one(),'record':gift_history.serialize_one(),'status':'OK'}
                    return jsonify (out)

                out = {'user':user.serialize_one(),'record':'','status':'not enough credit'}
                return jsonify (out)

            out = {'user':user.serialize_one(),'record':'','status':'gift has been finished'}
            return jsonify (out)

        out = {'user':user.serialize_one(),'record':'','status':'wrong gift id'}
        return jsonify (out)


app.add_url_rule('/api/shoppingresult/<int:gift_id>' , view_func = Shopping_Handler.buy_gift , methods = ['POST' , 'GET'])


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
            out = {'apps':Model.Android_Model.serialize_many(apps), 'status':'OK'}
            return jsonify (out)


        out = {'apps':'', 'status':'asscess denied'}
        return jsonify(out)


    @staticmethod
    @login_required
    def approve_or_reject (submit , app_id):

        app = Model.Android_Model.query.get (int (app_id))

        if submit == 'approve':

            app.approve()
            out = {'app':app.serialize_one() ,'submit':'approve','status':'OK'}
            return jsonify (out)


        elif submit == 'reject':

            app.reject()
            out = {'app':app.serialize_one() ,'submit':'reject','status':'OK'}
            return jsonify (out)



app.add_url_rule('/api/getPendingRequests' , view_func = Approve_System.get_pending_requests)
app.add_url_rule('/api/approveorreject/<string:submit>/<int:app_id>' , view_func = Approve_System.approve_or_reject )



class Gift_History_Manager:

    @staticmethod
    @login_required
    def gift_history_handler():

        user_id = session ['user_id']
        histories = Model.Gift_History_Model.query.filter_by (user_id = user_id)
        out = {'history':Model.Gift_History_Model.serialize_many(histories), 'status':'OK'}
        return jsonify (out)

app.add_url_rule('/api/gifthistory/' , view_func = Gift_History_Manager.gift_history_handler)


class Survey_Manager:

    @staticmethod
    @login_required
    def get_survey ():

        req = request.get_json()

        title = req ['name']
        description = req ['description']
        survey_questions = req ['questions']

        new_survey = Model.Survey_Model (title, description)
        new_survey.add_and_commit()

        for question in survey_questions:
            question_context = question ['context']
            question_items = question ['items']

            new_question = Model.Question_Model (question_context, new_survey.id)
            new_question.add_and_commit()

            for item in question_items:
                item_context = item ['context']
                new_item = Model.Item_Model (item_context, new_question.id)

        out = {'status':'OK'}

        return jsonify (out)


app.add_url_rule('/api/getSurvey' , view_func = Survey_Manager.get_survey , methods = ['GET','POST'])



@login_required
def show_survey():

    surveys = Model.Survey_Model.query.all()
    out = {'surveys':Model.Survey_Model.serialize_many(surveys),'status':'OK'}
    return jsonify (out)

app.add_url_rule('/api/showSurvey' , view_func = show_survey )


@login_required
def fill_survey (id):

    survey = Model.Survey_Model.query.get (id)
    out = {'survey':survey.serialize_one(), 'status':'OK'}

    return jsonify (out)

app.add_url_rule('/api/fillSurvey/<int:id>' , view_func = fill_survey )


@login_required
def submit_filling():
    req = request.get_json()
    #req is a dict of selected items
    #which each value in this dic, is item's primary_key (id)
    for key  in req:
        item = Model.Item_Model.query.get (int(req[key]))
        item.vote()

    out = {'status':'OK'}
    return jsonify (out)

app.add_url_rule('/api/submitFilling' , view_func = submit_filling , methods = ['GET','POST'])





if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run (debug = True)
    #app.run(host = '192.168.1.108' , port = 5000, debug = False)

# Correct Names
#Correct Survey_Manager
