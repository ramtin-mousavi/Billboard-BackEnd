from flask import request, jsonify, session, Blueprint
from flask_login import login_required

from Billboard.Apps.models import Android_Model
from Billboard.Survey.models import Survey_Model

from flask_cors import  cross_origin


admin = Blueprint('admin', __name__)


class Admin:

    @staticmethod
    @cross_origin(supports_credentials=True)
    @login_required
    def get_pending_apps():

        if session ['role'] == 'admin':

            apps = Android_Model.query_for_admin()
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

            surveys = Survey_Model.query_for_admin()
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



admin.add_url_rule('/api/getPendingApps' , view_func = Admin.get_pending_apps)
admin.add_url_rule('/api/approveOrRejectApps/<string:submit>/<int:app_id>' , view_func = Admin.approve_or_reject_apps )
admin.add_url_rule('/api/getPendingSurveys' , view_func = Admin.get_pending_surveys)
admin.add_url_rule('/api/approveOrRejectSurveys/<string:submit>/<int:survey_id>' , view_func = Admin.approve_or_reject_surveys )
