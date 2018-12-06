from Billboard import DataBase as db

from Billboard import MarshMallow as ma
from flask_marshmallow import Marshmallow

from datetime import datetime




class Gift_Model (db.Model):

    __tablename__ = 'gift_model'
    
    id = db.Column (db.Integer, primary_key = True)
    name =  db.Column(db.String(50), nullable = False)
    icon = db.Column (db.Text , nullable = False)
    code = db.Column (db.Text)
    description = db.Column (db.Text , nullable = False)
    supply = db.Column (db.Integer)
    cost = db.Column (db.Integer)


    def __init__ (self, name, icon, code, description, supply, cost):
        self.name = name
        self.icon = icon
        self.description = description
        self.supply = supply
        self.cost = cost
        self.code = code


    def discharge (self):
        if self.supply > 0 :
            self.supply -= 1
            db.session.commit()

    def charge (self, count):
        self.supply += count
        db.session.commit()


    def serialize_one (self):
        return Gift_Model_Schema().dump(self).data

    @staticmethod
    def serialize_many (arg):
        return Gift_Model_Schema(many = True).dump (arg).data



class Gift_Model_Schema (ma.ModelSchema):
    class Meta:
        model = Gift_Model




class Gift_History_Model (db.Model):

    __tablename__ = 'gift_history_model'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable = False)
    gift_id = db.Column(db.Integer, nullable = False)
    date = db.Column(db.DateTime, default = datetime.now)
    description = db.Column(db.Text, nullable=False)
    code = db.Column(db.Text)


    def __init__(self, user_id , giftId ):
        self.user_id = user_id
        self.gift_id = giftId
        self.description = Gift_Model.query.get (giftId).description
        self.code = Gift_Model.query.get (giftId).code


    def add_and_commit(self):
        db.session.add (self)
        db.session.commit()


    def serialize_one (self):
        return Gift_History_Model_Schema().dump(self).data

    @staticmethod
    def serialize_many (arg):
        return Gift_History_Model_Schema(many = True).dump (arg).data


class Gift_History_Model_Schema (ma.ModelSchema) :
    class Meta:
        model = Gift_History_Model
