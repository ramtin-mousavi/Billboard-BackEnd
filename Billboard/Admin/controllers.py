from flask import request, jsonify, session, Blueprint
from flask_login import login_required

from Billboard.Authentication.models import User_Model
from Billboard.Apps.models import Android_Model
from Billboard.Survey.models import Survey_Model

from flask_cors import  cross_origin

from datetime import datetime, timedelta

admin = Blueprint('admin', __name__)



class AdminDecorator:
    def __init__ (self, params):
        self.params = params

    def __call__ (self, f):

        def wrapped_f ():
            if session ['role'] == 'admin':
                return f()
            else:
                out = {}
                for param in self.params :
                    out [param] = ''
                out ['status'] = 'access denied'

                return jsonify (out)
        wrapped_f.__name__ = f.__name__
        return wrapped_f
        

class Admin:

    @staticmethod
    @cross_origin(supports_credentials=True)
    @login_required
    def get_pending_apps():

        if session ['role'] == 'admin':

            apps = Android_Model.query_ ('pending')
            out = {'apps':Android_Model.serialize_many(apps), 'status':'OK'}
            return jsonify (out)


        out = {'apps':'', 'status':'asscess denied'}
        return jsonify(out)


    @staticmethod
    @cross_origin(supports_credentials=True)
    @login_required
    def approve_or_reject_apps (submit , app_id):

        if session ['role'] == 'admin':

            app = Android_Model.query.get (int (app_id))

            if app:

                if submit == 'approve':

                    app.approve()
                    out = {'app':app.serialize_one() ,'submit':'approve','status':'OK'}
                    return jsonify (out)


                elif submit == 'reject':

                    app.reject()
                    out = {'app':app.serialize_one() ,'submit':'reject','status':'OK'}
                    return jsonify (out)

                out = {'app':'', 'submit':'', 'status':'submit command is wrong'}
                return jsonify (out)

            out = {'app':'', 'submit':'', 'status':'app id is wrong'}
            return jsonify (out)

        out = {'app':'', 'submit':'' ,'status':'asscess denied'}
        return jsonify(out)


    @staticmethod
    @cross_origin(supports_credentials=True)
    @login_required
    def get_pending_surveys ():

        if session ['role'] == 'admin':

            surveys = Survey_Model.query_('pending')
            out = {'surveys':Survey_Model.serialize_many(surveys), 'status':'OK'}
            return jsonify (out)


        out = {'surveys':'', 'status':'asscess denied'}
        return jsonify(out)


    @staticmethod
    @cross_origin(supports_credentials=True)
    @login_required
    def approve_or_reject_surveys (submit , survey_id):

        if session ['role'] == 'admin':

            survey = Survey_Model.query.get (int (survey_id))

            if survey:

                if submit == 'approve':

                    survey.approve()
                    out = {'survey':survey.serialize_one() ,'submit':'approve','status':'OK'}
                    return jsonify (out)


                elif submit == 'reject':

                    survey.reject()
                    out = {'survey':survey.serialize_one() ,'submit':'reject','status':'OK'}
                    return jsonify (out)

                out = {'survey':'', 'submit':'', 'status':'submit command is wrong'}
                return jsonify (out)

            out = {'survey':'', 'submit':'', 'status':'app id is wrong'}
            return jsonify (out)

        out = {'survey':'', 'submit':'' ,'status':'asscess denied'}
        return jsonify(out)


    @staticmethod
    @cross_origin(supports_credentials=True)
    @login_required
    def get_users_count ():

        if session ['role'] == 'admin':
            out = {'user_count':User_Model.query.count(), 'status':'OK'}
            return jsonify (out)

        out = {'user_count':'', 'status':'access denied'}
        return jsonify (out)


    @staticmethod
    @cross_origin(supports_credentials=True)
    @login_required
    def active_ads_count ():

        if session['role'] == 'admin':
            surveys = Survey_Model.query_ ('approved').count()
            apps = Android_Model.query_ ('approved').count()

            out = {'ads_count':surveys + apps, 'status':'OK'}
            return jsonify (out)

        out = {'ads_count':'', 'status':'access denied'}
        return jsonify (out)


    @staticmethod
    @cross_origin(supports_credentials=True)
    @login_required
    def today_ads_count ():

        if session['role'] == 'admin':

            today = datetime.now()
            today_start = datetime (today.year, today.month, today.day, 00, 00, 00)
            today_stop = datetime (today.year, today.month, today.day, 23, 59, 59)

            count = (Android_Model.query.filter (Android_Model.advertise_date > today_start,
                    Android_Model.advertise_date < today_stop).count()
                    )
            count += (Survey_Model.query.filter (Survey_Model.advertise_date > today_start,
                    Survey_Model.advertise_date < today_stop).count()
                    )

            out = {'today_ads_count':count, 'status': 'OK'}
            return jsonify (out)

        out = {'today_ads_count':'', 'status':'access denied'}
        return jsonify (out)


admin.add_url_rule('/api/getPendingApps' , view_func = Admin.get_pending_apps)
admin.add_url_rule('/api/approveOrRejectApps/<string:submit>/<int:app_id>' , view_func = Admin.approve_or_reject_apps )
admin.add_url_rule('/api/getPendingSurveys' , view_func = Admin.get_pending_surveys)
admin.add_url_rule('/api/approveOrRejectSurveys/<string:submit>/<int:survey_id>' , view_func = Admin.approve_or_reject_surveys )
admin.add_url_rule ('/api/userCount', view_func=Admin.get_users_count)
admin.add_url_rule ('/api/adsCount', view_func=Admin.active_ads_count)
admin.add_url_rule ('/api/todayAdsCount', view_func=Admin.today_ads_count)
