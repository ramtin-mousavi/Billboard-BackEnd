import sys
sys.path.append("..")

from Models import Model
from flask_login import login_required, login_user, logout_user , LoginManager, current_user
from flask import Flask, flash, redirect, render_template, request, url_for , make_response


class Load_User:

    @staticmethod
    @login_manager.user_loader
    def load_user(userid):
        return Model.User_Model.query.get(int(userid))



class Main :

    @staticmethod
    def home_page():
        if current_user.is_authenticated:
            return redirect (url_for('show_apps' , page_numb = 1))

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
                apps = Android_Model.paginate_by_filter (8,page_numb,True,'Game')
                return render_template ('profile.html', user = Load_User.load_user (current_user.id) , apps = apps)

            elif int (req) == 2:
                apps = Android_Model.paginate_by_filter (8,page_numb,True,'App')
                return render_template ('profile.html', user = Load_User.load_user (current_user.id) , apps = apps)

            elif int ( req ) == 1:
                apps = Android_Model.paginate_query (8,page_numb,True)
                return render_template ('profile.html', user = Load_User.load_user (current_user.id) , apps = apps)

        # If No Filter
        else:
            apps = Android_Model.paginate_query (8,page_numb,True)
            return render_template ('profile.html', user = Load_User.load_user (current_user.id) , apps = apps)


class Show_Gifts_Manager:

    @staticmethod
    @login_required
    def show_gifts (page_numb):

        gifts = Gift_Model.paginate_query (8, page_numb, True)
        return render_template ('giftshop.html' ,user = Load_User.load_user (current_user.id) , gifts = gifts)




class Shopping_Handler:

    @staticmethod
    @login_required
    def buy_gift (id):

        temp_gift = Gift_Model.id_query (id)

        if temp_gift.supply > 0:
            user = Load_User.load_user (current_user.id)

            if user.credit > temp_gift.cost:

                giftHistory = Gift_History_Model (user.id , temp_gift.id)
                giftHistory.add_and_commit()

                user.discharge (temp_gift.cost)
                temp_gift.discharge()

                return render_template ('giftresult.html' , gift = temp_gift)

            flash ('اعتبار شما کافي نيست')
            return redirect (url_for('show_apps' , page_numb = 1))

        return "In Gift Tamum Shode!"


class Advertising :

    @staticmethod
    @login_required
    def request_new_ad ():

        return render_template ('submit_new_ad.html')


    @staticmethod
    @login_required
    def submit_new_ad ():

        submit_form = Submit_Form (request.form)

        if submit_form.validate ():
            if request.method == 'POST' :

                new_app = Android_Model (request.form ['name'] , request.form ['iconlink'] , 'App' , 100 , request.form ['dllink'] , request.form ['deeplink'] ,
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

            apps = Android_Model.paginate_query_for_admin (8 , page_numb , True)
            return render_template ('adminPendingRequests.html' , apps = apps)


        return "Access Denied"


    @staticmethod
    @login_required
    def approve_or_reject (id):

        app = Android_Model.query.get (id)
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



################## Do It Using Foreign Key ##############
class Gift_History_Manager:

    @staticmethod
    @login_required
    def gift_history_handler(page_numb):

        user = Load_User.load_user (current_user.id)
        user_id = user.id
        gifts = Gift_History_Model.paginate_query(8, page_numb, True, user_id)

        return render_template('NewHistory.html', gifts = gifts , user = user)


class Survey_Manager:

    @staticmethod
    @login_required
    def add_survey ():

        return render_template ('temp.html')


    @staticmethod
    @login_required
    def get_survey ():

        count = request.form ['questions_count']
        survey = Survey_Model (request.form ['question_name'] , 'description')
        survey.add_and_commit()

        for question_number in range (int(count)):

            new_question = Question_Model (request.form ['q'+str(question_number)] , survey.id)
            new_question.add_and_commit()

            for item in request.form.getlist('item'+str(question_number)):

                new_item = Item_Model (item , new_question.id)
                new_item.add_and_commit()


        return "DONE"
