from flask import request, jsonify, session, Blueprint
from flask_login import login_required

from Billboard.Apps.models import Android_Model


admin = Blueprint('admin', __name__)


class Admin:

    @staticmethod
    @login_required
    def get_pending_requests():

        if session ['role'] == 'admin':

            apps = Android_Model.query_for_admin()
            out = {'apps':Android_Model.serialize_many(apps), 'status':'OK'}
            return jsonify (out)


        out = {'apps':'', 'status':'asscess denied'}
        return jsonify(out)


    @staticmethod
    @login_required
    def approve_or_reject (submit , app_id):

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


admin.add_url_rule('/api/getPendingRequests' , view_func = Admin.get_pending_requests)
admin.add_url_rule('/api/approveorreject/<string:submit>/<int:app_id>' , view_func = Admin.approve_or_reject )
