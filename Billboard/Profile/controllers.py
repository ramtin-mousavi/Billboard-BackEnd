from flask import request, jsonify, session, Blueprint
from flask_login import login_required

from Billboard.Apps.models import Android_Model
from Billboard.Survey.models import Survey_Model, Question_Model, Item_Model

from flask_cors import  cross_origin


profile = Blueprint('profile', __name__)


class Advertise_Stat:

    @staticmethod
    @cross_origin(supports_credentials=True)
    @login_required
    def get_advertised_apps():

        apps = Android_Model.serialize_many(Android_Model.query_('all',advertiser_id = session['user_id']))
        out = {'apps':apps, 'status':'OK'}
        return jsonify (out)


    @staticmethod
    @cross_origin(supports_credentials=True)
    @login_required
    def get_advertised_surveys():

        surveys = Survey_Model.serialize_many(Survey_Model.query_('all', advertiser_id = session['user_id']))
        out = {'surveys':surveys, 'status':'OK'}
        return jsonify (out)


    @staticmethod
    @cross_origin(supports_credentials=True)
    @login_required
    def get_app_stat (app_id):

        app = Android_Model.query.get (app_id)
        if app:

            if app in Android_Model.query_ ('all', advertiser_id = session['user_id']):

                if app.approval_status == 'pending':
                    out = {'app_stat':app.serialize_one(), 'status':'app is waiting to be submitted'}
                    return jsonify (out)

                elif app.approval_status == 'rejected':
                    out = {'app_stat':app.serialize_one(), 'status':'app has been rejected'}
                    return jsonify (out)

                else:

                    out = {'app_stat':app.serialize_one(), 'status':'OK'}
                    return jsonify (out)

            out = {'app_stat':'', 'status':'you are not the advertiser of this app'}
            return jsonify (out)

        out = {'app_stat':'', 'status':'wrong app_id'}
        return jsonify (out)


    @staticmethod
    @cross_origin(supports_credentials=True)
    @login_required
    def get_survey_stat (survey_id):

        survey = Survey_Model.query.get (survey_id)

        if survey:

            if survey in Survey_Model.query_ ('all', advertiser_id = session['user_id']):

                if survey.approval_status == 'pending':
                    out = {'survey_stat':survey.serialize_one(), 'status':'survey is waiting to be submitted'}
                    return jsonify (out)

                elif survey.approval_status == 'rejected':
                    out = {'survey_stat':survey.serialize_one(), 'status':'survey has been rejected'}
                    return jsonify (out)

                else:

                    out = {'survey_stat':survey.serialize_one(), 'status':'OK'}
                    return jsonify (out)

            out = {'app_stat':'', 'status':'you are not the advertiser of this survey'}
            return jsonify (out)

        out = {'survey_stat':'', 'status':'wrong survey_id'}
        return jsonify (out)


profile.add_url_rule('/api/getAdvertisedApps' , view_func = Advertise_Stat.get_advertised_apps )
profile.add_url_rule('/api/getAdvertisedSurveys' , view_func = Advertise_Stat.get_advertised_surveys )
profile.add_url_rule('/api/getAppStat/<int:app_id>' , view_func = Advertise_Stat.get_app_stat)
profile.add_url_rule('/api/getSurveyStat/<int:survey_id>' , view_func = Advertise_Stat.get_survey_stat)


class Advertising:

    @staticmethod
    @cross_origin(supports_credentials=True)
    @login_required
    def advertise_survey ():

        req = request.get_json(force = True)

        title = req ['name']
        description = req ['description']
        credit = int (req ['credit'])
        duration = int (req ['duration'])
        survey_questions = req ['questions']
        user_id = session['user_id']

        new_survey = Survey_Model (title, description, user_id, duration, credit)
        new_survey.add_and_commit()

        for question in survey_questions:
            question_context = question ['context']
            question_items = question ['items']

            new_question = Question_Model (question_context, new_survey.id)
            new_question.add_and_commit()

            for item in question_items:
                item_context = item ['context']
                new_item = Item_Model (item_context, new_question.id)
                new_item.add_and_commit()

        out = {'status':'OK'}

        return jsonify (out)


    @staticmethod
    @cross_origin(supports_credentials=True)
    @login_required
    def advertise_app():

        req = request.get_json(force = True)
        user_id = session ['user_id']
        new_app = Android_Model (req['name'],str(req['name']), req['icon'], req['category'], int(req['credit']), req['dlLink'], user_id, int(req['duration']))
        new_app.add_and_commit()


        out = {'status':'OK'}
        return jsonify (out)




profile.add_url_rule('/api/getSurvey' , view_func = Advertising.advertise_survey , methods = ['GET','POST'])
profile.add_url_rule('/api/getApp' , view_func = Advertising.advertise_app , methods = ['GET','POST'])
