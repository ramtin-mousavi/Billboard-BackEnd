from flask import request, jsonify, session, Blueprint
from flask_login import login_required

from Billboard.Survey.models import Item_Model, Question_Model, Survey_Model
from Billboard.Authentication.models import User_Model


surveys = Blueprint('surveys', __name__)


class Survey_Manager:

    @staticmethod
    @login_required
    def show_survey():

        surveys = Survey_Model.query_for_user(User_Model.query.get (session['user_id']))
        if (len (surveys) != 0):
            out = {'surveys':Survey_Model.serialize_many(surveys),'status':'OK'}
            return jsonify (out)

        out = {'surveys':'', 'status':'no survey to show for this user'}
        return jsonify (out)


    @staticmethod
    @login_required
    def fill_survey (id):

        user = User_Model.query.get (session['user_id'])
        survey = Survey_Model.query.get (id)
        if survey:
            if (survey not in user.submitted_surveys):
                out = {'survey':survey.serialize_one(), 'status':'OK'}
                return jsonify (out)

            out = {'survey':'', 'status':'user has already filled this survey'}
            return jsonify (out)

        out = {'survey':'', 'status':'invalid survey id'}
        return jsonify (out)


    @staticmethod
    @login_required
    def submit_filling():

        req = request.get_json(force = True).get('items')

        if len(req) > 0:
            itm = Item_Model.query.get (int(req[0]))
            survey = Survey_Model.query.get((Question_Model.query.get(itm.question_id)).survey_id)
            user = User_Model.query.get (session['user_id'])

            if survey not in user.submitted_surveys:

                # req is a list of selected items
                #which each value in this list, is item's primary_key (id)
                for pk in req:
                    item = Item_Model.query.get (int (pk))
                    item.vote()

                #add user to survey's users
                user.append_survey (survey)

                out = {'status':'OK'}
                return jsonify (out)

            out = {'status':'user has already filled this survey'}
            return jsonify (out)

        out = {'status':'item list is empty'}
        return jsonify (out)


surveys.add_url_rule('/api/getSurvey' , view_func = Survey_Manager.get_survey , methods = ['GET','POST'])
surveys.add_url_rule('/api/showSurvey' , view_func = Survey_Manager.show_survey )
surveys.add_url_rule('/api/fillSurvey/<int:id>' , view_func = Survey_Manager.fill_survey )
surveys.add_url_rule('/api/submitFilling' , view_func = Survey_Manager.submit_filling , methods = ['GET','POST'])
