from flask import request, jsonify, session, Blueprint
from flask_login import login_required

from Billboard.Apps.models import Android_Model

apps = Blueprint('apps', __name__)


class Apps_Manager:

    @staticmethod
    @login_required
    def show_apps (filter=None):

        if filter:
            if int (filter) == 3:
                apps = Android_Model.filter_query ('Game')
                out = {'apps':Android_Model.serialize_many (apps) , 'status': 'OK'}
                return jsonify (out)

            elif int (filter) == 2:
                apps = Android_Model.filter_query ('App')
                out = {'apps':Android_Model.serialize_many (apps) , 'status': 'OK'}
                return jsonify (out)

            elif int (filter) == 1:
                apps = Android_Model.all_query()
                out = {'apps':Android_Model.serialize_many (apps) , 'status': 'OK'}
                return jsonify (out)

            else:
                out = {'apps':'', 'status':'filter is not valid'}
                return jsonify (out)

        apps = Android_Model.all_query()
        out = {'apps':Android_Model.serialize_many (apps) , 'status': 'OK'}
        return jsonify (out)


apps.add_url_rule('/api/showApps/<int:filter>' , view_func = Apps_Manager.show_apps)
apps.add_url_rule('/api/showApps/' , view_func = Apps_Manager.show_apps)