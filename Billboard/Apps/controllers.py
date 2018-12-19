from flask import request, jsonify, session, Blueprint
from flask_login import login_required

from Billboard.Apps.models import Android_Model
from flask_cors import  cross_origin

apps = Blueprint('apps', __name__)


class Apps_Manager:

    @staticmethod
    @cross_origin(supports_credentials=True)
    @login_required
    def show_apps (filter=None):

        if filter:
            if int (filter) == 3:
                apps = Android_Model.query_ ('approved', filt = 'Game')
                out = {'apps':Android_Model.serialize_many (apps) , 'status': 'OK'}
                return jsonify (out)

            elif int (filter) == 2:
                apps = Android_Model.query_ ('approved', filt = 'App')
                out = {'apps':Android_Model.serialize_many (apps) , 'status': 'OK'}
                return jsonify (out)

            elif int (filter) == 1:
                apps = Android_Model.query_ ('approved')
                out = {'apps':Android_Model.serialize_many (apps) , 'status': 'OK'}
                return jsonify (out)

            else:
                out = {'apps':'', 'status':'filter is not valid'}
                return jsonify (out)

        apps = Android_Model.query_ ('approved')
        out = {'apps':Android_Model.serialize_many (apps) , 'status': 'OK'}
        return jsonify (out)


apps.add_url_rule('/api/showApps/<int:filter>' , view_func = Apps_Manager.show_apps)
apps.add_url_rule('/api/showApps/' , view_func = Apps_Manager.show_apps)
