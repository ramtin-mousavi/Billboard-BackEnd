from flask import request, jsonify, session, Blueprint
from flask_login import login_required

from Billboard.Apps.models import Android_Model
from Billboard.Survey.models import Survey_Model


profile = Blueprint('profile', __name__)


class Advertise_Stat:

    @staticmethod
    @login_required
    def get_advertised_apps():

        apps = Android_Model.serialize_many(Android_Model.query_for_advertiser(session['user_id']))
        out = {'apps':apps, 'status':'OK'}
        return jsonify (out)


    @staticmethod
    @login_required
    def get_advertised_surveys():

        surveys = Survey_Model.serialize_many(Survey_Model.query_for_advertiser(['user_id']))
        out = {'surveys':surveys, 'status':'OK'}
        return jsonify (out)


    @staticmethod
    @login_required
    def get_app_stat (app_id):

        app = Android_Model.query.get (app_id)

        if app:

            if app.approval_status == 'pending':
                out = {'app_stat':app.serialize_one(), 'status':'app is waiting to be submitted'}
                return jsonify (out)

            elif app.approval_status == 'rejected':
                out = {'app_stat':app.serialize_one(), 'status':'app has been rejected'}
                return jsonify (out)

            else:

                out = {'app_stat':app.serialize_one(), 'status':'OK'}
                return jsonify (out)

        out = {'app_stat':'', 'status':'wrong app_id'}
        return jsonify (out)


    @staticmethod
    @login_required
    def get_survey_stat (survey_id):

        survey = Survey_Model.query.get (survey_id)

        if app:

            if survey.approval_status == 'pending':
                out = {'survey_stat':survey.serialize_one(), 'status':'survey is waiting to be submitted'}
                return jsonify (out)

            elif survey.approval_status == 'rejected':
                out = {'survey_stat':survey.serialize_one(), 'status':'survey has been rejected'}
                return jsonify (out)

            else:

                out = {'survey_stat':survey.serialize_one(), 'status':'OK'}
                return jsonify (out)

        out = {'survey_stat':'', 'status':'wrong survey_id'}
        return jsonify (out)


profile.add_url_rule('/api/getAdvertisedApps' , view_func = Advertise_Stat.get_advertised_apps )
profile.add_url_rule('/api/getAdvertisedSurveys' , view_func = Advertise_Stat.get_advertised_surveys )
profile.add_url_rule('/api/getAppStat/<int:app_id>' , view_func = Advertise_Stat.get_app_stat)
profile.add_url_rule('/api/getAppStat/<int:survey_id>' , view_func = Advertise_Stat.get_survey_stat)


class Advertising:

    pass
