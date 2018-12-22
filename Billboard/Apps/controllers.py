from flask import request, jsonify, session, Blueprint
from flask_login import login_required

from Billboard.Apps.models import Android_Model
from Billboard.Authentication.models import User_Model

from flask_cors import  cross_origin

apps = Blueprint('apps', __name__)


class Apps_Manager:

    @staticmethod
    @cross_origin(supports_credentials=True)
    @login_required
    def show_apps (filter=None):

        user = User_Model.query.get (session['user_id'])

        if filter:
            if int (filter) == 3:
                apps = Android_Model.query_ ('approved', filt = 'Game', user = user)
                out = {'apps':Android_Model.serialize_many (apps) , 'status': 'OK'}
                return jsonify (out)

            elif int (filter) == 2:
                apps = Android_Model.query_ ('approved', filt = 'App', user = user)
                out = {'apps':Android_Model.serialize_many (apps) , 'status': 'OK'}
                return jsonify (out)

            elif int (filter) == 1:
                apps = Android_Model.query_ ('approved', user = user)
                out = {'apps':Android_Model.serialize_many (apps) , 'status': 'OK'}
                return jsonify (out)

            else:
                out = {'apps':'', 'status':'filter is not valid'}
                return jsonify (out)

        apps = Android_Model.query_ ('approved', user = user)
        out = {'apps':Android_Model.serialize_many (apps) , 'status': 'OK'}
        return jsonify (out)


    @staticmethod
    @cross_origin(supports_credentials=True)
    @login_required
    def install_app (app_id):



        #package_name = request.get_json(force = True).get('package_name')
        user = User_Model.query.get (session['user_id'])
        #app = Android_Model.query_by_package_name (package_name)
        app = Android_Model.query.get (int(app_id))

        if app:
            if app not in user.installed_android_apps:

                user.append_android_app (app)
                user.charge (app.credit)
                app.increment_count()

                out = {'app':app.serialize_one(), 'status':'OK'}
                return jsonify (out)


            out = {'app':'', 'status':'user has already installed this app'}
            return jsonify (out)

        out = {'app':'', 'status':'wrong app_id'}
        return jsonify (out)




apps.add_url_rule('/api/showApps/<int:filter>' , view_func = Apps_Manager.show_apps)
apps.add_url_rule('/api/showApps/' , view_func = Apps_Manager.show_apps)
apps.add_url_rule('/api/installApp/<int:app_id>' , view_func = Apps_Manager.install_app)
