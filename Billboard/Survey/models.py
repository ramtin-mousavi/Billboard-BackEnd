from Billboard import DataBase as db

from Billboard import MarshMallow as ma
from flask_marshmallow import Marshmallow

from datetime import datetime, timedelta



class Item_Model (db.Model):

    __tablename__ = 'item_model'

    id = db.Column(db.Integer, primary_key = True)
    context = db.Column (db.Text , nullable = False)
    question_id = db.Column(db.Integer, db.ForeignKey('question_model.id'), nullable=False)
    vote_count = db.Column (db.Integer , nullable = False)

    def __init__ (self , context , question_id):
        self.context = context
        self.question_id = question_id
        self.vote_count = 0


    def vote (self):
        self.vote_count += 1
        db.session.commit()


    def add_and_commit (self):
        db.session.add (self)
        db.session.commit()


    def serialize_one (self):
        return Item_Model_Schema().dump(self).data

    @staticmethod
    def serialize_many (arg):
        return Item_Model_Schema(many = True).dump (arg).data


class Item_Model_Schema (ma.ModelSchema):

    class Meta:
        model = Item_Model




class Question_Model (db.Model):

    __tablename__ = 'question_model'

    id = db.Column(db.Integer, primary_key = True)
    context = db.Column (db.Text , nullable = False)
    items = db.relationship ('Item_Model' , backref = 'question_model' , lazy = True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey_model.id'), nullable=False)

    def __init__ (self , context , survey_id):
        self.context = context
        self.survey_id = survey_id


    def add_and_commit (self):
        db.session.add (self)
        db.session.commit()


    def serialize_one (self):
        return Question_Model_Schema().dump(self).data

    @staticmethod
    def serialize_many (arg):
        return Question_Model_Schema(many = True).dump (arg).data



class Question_Model_Schema (ma.ModelSchema):

    items = ma.Nested(Item_Model_Schema, many = True)
    class Meta:
        model = Question_Model




class Survey_Model (db.Model):

    __tablename__ = 'survey_model'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column (db.String(40), nullable = False)
    description = db.Column (db.Text , nullable = False)
    advertiser_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
    questions = db.relationship ('Question_Model' , backref = 'survey_model' , lazy = True)
    approval_status = db.Column (db.String(20), nullable = False)
    credit = db.Column (db.Integer , nullable = False)
    advertise_date = db.Column(db.DateTime)
    expiration_date = db.Column(db.DateTime)

    def __init__ (self , title , description, advertiser_id, duration, credit):
        self.title = title
        self.description = description
        self.approval_status = 'pending'
        self.credit = credit
        self.advertiser_id = advertiser_id
        self.advertise_date = datetime.now()
        self.expiration_date = self.advertise_date + timedelta (days = duration)

    def approve (self):
        self.approval_status = 'approved'
        db.session.commit()

    def reject (self):
        self.approval_status = 'rejected'
        db.session.commit()

    def expire (self):
        self.approval_status = 'expired'
        db.session.commit()

    def add_and_commit (self):
        db.session.add (self)
        db.session.commit()

    def calculate_cost (self):

        duration = (self.expiration_date - self.advertise_date).days
        cost = (20 * duration * self.credit) // ((duration % 10))

        return cost


    @staticmethod
    def query_ (status, user = None, advertiser_id = None):

        assert (status in ['approved', 'rejected', 'pending', 'all'])

        if user:
            surveys = Survey_Model.query.filter_by (approval_status = status)
            surveys_to_show = []
            for survey in surveys:
                if survey not in user.submitted_surveys:
                    surveys_to_show.append (survey)

            return surveys_to_show

        if advertiser_id:
            return Survey_Model.query.filter_by (advertiser_id = advertiser_id)

        return Survey_Model.query.filter_by (approval_status = status)



    def serialize_one (self):
        return Survey_Model_Schema().dump(self).data

    @staticmethod
    def serialize_many (arg):
        return Survey_Model_Schema(many = True).dump (arg).data


class Survey_Model_Schema (ma.ModelSchema):

    questions = ma.Nested(Question_Model_Schema, many = True)

    class Meta:
        model = Survey_Model
