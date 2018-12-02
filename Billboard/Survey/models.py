from Billboard import DataBase as db

from Billboard import MarshMallow as ma
from flask_marshmallow import Marshmallow

from Billboard.Authentication.models import User_Model


#many to many relationship between users and surveys
user_survey_table = db.Table ('user_survey_table',
db.Column('user_id', db.Integer, db.ForeignKey('survey_model.id')),
db.Column('survey_id', db.Integer, db.ForeignKey('user_model.id'))
)




class Item_Model (db.Model):

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
    # foreign key to user
    questions = db.relationship ('Question_Model' , backref = 'survey_model' , lazy = True)
    approval_status = db.Column (db.String(20), nullable = False)
    credit = db.Column (db.Integer , nullable = False)

    users = db.relationship("User_Model", secondary = user_survey_table)

    def __init__ (self , title , description ):
        self.title = title
        self.description = description
        self.approval_status = 'pending'
        self.credit = 100

    def approve (self):
        self.approval_status = 'approved'
        db.session.commit()

    def reject (self):
        self.approval_status = 'rejected'
        db.session.commit()

    def add_and_commit (self):
        db.session.add (self)
        db.session.commit()

    def append_user (self,user):
        self.users.append (user)
        db.session.commit()

    def serialize_one (self):
        return Survey_Model_Schema().dump(self).data

    @staticmethod
    def serialize_many (arg):
        return Survey_Model_Schema(many = True).dump (arg).data

    @staticmethod
    def query_for_admin():
        return Survey_Model.query.filter (Survey_Model.approval_status == 'pending')

    @staticmethod
    def query_for_user (user):

        approved_surveys = Survey_Model.query.filter (Survey_Model.approval_status == 'approved')
        surveys_to_show = []
        for survey in approved_surveys:
            if user not in survey.users:
                surveys_to_show.append (survey)

        return surveys_to_show



class Survey_Model_Schema (ma.ModelSchema):

    questions = ma.Nested(Question_Model_Schema, many = True)

    class Meta:
        model = Survey_Model
        exclude = ('users','approval_status')
