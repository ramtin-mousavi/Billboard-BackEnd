from flask import request, jsonify, session, Blueprint
from flask_login import login_required
from Billboard.Admin.controllers import Admin_Required

from Billboard.Ticketing.models import Ticket_Model

from flask_cors import  cross_origin

tickets = Blueprint('tickets', __name__)


class Ticketing:

    @staticmethod
    @cross_origin (supports_credentials = True)
    @login_required
    def send_ticket ():

        req = request.get_json(force = True)
        new_ticket = Ticket_Model (req['title'], req['description'], session ['user_id'])
        new_ticket.add_and_commit()

        out = {'status':'OK'}
        return jsonify (out)

    @staticmethod
    @cross_origin (supports_credentials = True)
    @login_required
    def get_my_tickets ():

        my_tickets = Ticket_Model.query_ (2, user_id = int(session['user_id']))
        if my_tickets :
            out = {'tickets': Ticket_Model.serialize_many(my_tickets), 'status':'OK'}
            return jsonify (out)

        out = {'tickets':'', 'status':'you have no tickets'}
        return jsonify (out)


    @staticmethod
    @cross_origin (supports_credentials = True)
    @login_required
    def get_my_answered_tickets ():
        my_tickets = Ticket_Model.query_ (1, user_id = int(session['user_id']))
        if my_tickets :
            out = {'tickets': Ticket_Model.serialize_many(my_tickets), 'status':'OK'}
            return jsonify (out)

        out = {'tickets':'', 'status':'you have no tickets'}
        return jsonify (out)


    @staticmethod
    @cross_origin (supports_credentials = True)
    @login_required
    @Admin_Required (['tickets'])
    def get_all_tickets ():

        tickets = Ticket_Model.query_ (2)
        if tickets :
            out = {'tickets': Ticket_Model.serialize_many(tickets), 'status':'OK'}
            return jsonify (out)

        out = {'tickets':'', 'status':'there are no tickets'}
        return jsonify (out)



    @staticmethod
    @cross_origin (supports_credentials = True)
    @login_required
    @Admin_Required (['tickets'])
    def get_non_answered_tickets ():

        tickets = Ticket_Model.query_ (0)
        if tickets :
            out = {'tickets': Ticket_Model.serialize_many(tickets), 'status':'OK'}
            return jsonify (out)

        out = {'tickets':'', 'status':'there are no tickets'}
        return jsonify (out)



    @staticmethod
    @cross_origin (supports_credentials = True)
    @login_required
    @Admin_Required ([])
    def answer_ticket ():

        req = request.get_json(force = True)
        ticket = Ticket_Model.query.get (int (req['ticket_id']))
        if ticket:
            if ticket.is_answered :
                out = {'status':'ticket has been already answered'}
                return jsonify (out)

            ticket.answer(req['answer'])
            out = {'status':'OK'}
            return jsonify (out)

        out = {'status':'invalid ticket id'}
        return jsonify (out)




tickets.add_url_rule('/api/sendTicket' , view_func = Ticketing.send_ticket , methods = ['GET','POST'])
tickets.add_url_rule('/api/getMyTickets' , view_func = Ticketing.get_my_tickets)
tickets.add_url_rule('/api/getMyAnsweredTickets' , view_func = Ticketing.get_my_answered_tickets)
tickets.add_url_rule('/api/getAllTickets' , view_func = Ticketing.get_all_tickets)
tickets.add_url_rule('/api/getNonAnsweredTickets' , view_func = Ticketing.get_non_answered_tickets)
tickets.add_url_rule('/api/answerTicket' , view_func = Ticketing.answer_ticket , methods = ['GET','POST'])
