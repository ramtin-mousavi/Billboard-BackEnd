from flask import request, jsonify, session, Blueprint
from flask_login import login_required

from Billboard.Gifts.models import Gift_Model, Gift_History_Model
from Billboard.Authentication.models import User_Model

from flask_cors import  cross_origin


gifts = Blueprint('gifts', __name__)



class Gift_Manager:

    @staticmethod
    @cross_origin(supports_credentials=True)
    @login_required
    def show_gifts ():

        gifts = Gift_Model.query.filter(Gift_Model.supply > 0)
        out = {'gifts':Gift_Model.serialize_many(gifts), 'status':'OK'}
        return jsonify (out)


    @staticmethod
    @cross_origin(supports_credentials=True)
    @login_required
    def buy_gift (gift_id):

        temp_gift = Gift_Model.query.get (int(gift_id))
        if temp_gift:
            if temp_gift.supply > 0:

                user = User_Model.query.get (session['user_id'])

                if user.credit > temp_gift.cost:

                    user.discharge (temp_gift.cost)
                    temp_gift.discharge()

                    #Save Transaction Record
                    gift_history = Gift_History_Model (user.id , temp_gift.id)
                    gift_history.add_and_commit()

                    out = {'record':gift_history.serialize_one(),'status':'OK'}
                    return jsonify (out)

                out = {'record':'','status':'not enough credit'}
                return jsonify (out)

            out = {'record':'','status':'gift has been finished'}
            return jsonify (out)

        out = {'record':'','status':'wrong gift id'}
        return jsonify (out)


    @staticmethod
    @cross_origin(supports_credentials=True)
    @login_required
    def gift_history():

        user_id = session ['user_id']
        histories = Gift_History_Model.query.filter_by (user_id = user_id)
        out = {'history':Gift_History_Model.serialize_many(histories), 'status':'OK'}
        return jsonify (out)


gifts.add_url_rule('/api/giftshop' , view_func = Gift_Manager.show_gifts )
gifts.add_url_rule('/api/shoppingresult/<int:gift_id>' , view_func = Gift_Manager.buy_gift , methods = ['POST' , 'GET'])
gifts.add_url_rule('/api/gifthistory' , view_func = Gift_Manager.gift_history)
