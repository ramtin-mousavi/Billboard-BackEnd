from Billboard import DataBase as db

from Billboard import MarshMallow as ma
from flask_marshmallow import Marshmallow


class Ticket_Model (db.Model):
    __tablename__ = 'ticket_model'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column (db.String(40), nullable = False)
    description = db.Column (db.Text , nullable = False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
    answer = db.Column (db.Text)
    is_answered = db.Column (db.Boolean, nullable = False)


    def __init__ (self, title, description, sender_id):
        self.title = title
        self.description = description
        self.sender_id = sender_id
        self.is_answered = False

    def add_and_commit (self):
        db.session.add (self)
        db.session.commit()


    def answer (self, ans):
        self.answer = ans
        self.is_answered = True
        db.session.commit()


    def _query (status = False, user_id = None):

        if user_id:         #_query(user_id) for users to see all tickets
            return Ticket_Model.query.filter_by (sender_id = user_id)

        if status:      #_query (status=True) for admin to see answered tickets
            return Ticket_Model.query.filter_by (is_answered = True)
            
        #_query () for admin to see non answered tickets
        return Ticket_Model.query.filter_by (is_answered = False)



    def serialize_one (self):
        return Ticket_Model_Schema().dump(self).data

    @staticmethod
    def serialize_many (arg):
        return Ticket_Model_Schema(many = True).dump (arg).data


class Ticket_Model_Schema (ma.ModelSchema):

    class Meta:
        model = Ticket_Model
