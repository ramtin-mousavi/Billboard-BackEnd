from Billboard import DataBase as db

from flask_login import UserMixin
from werkzeug import generate_password_hash, check_password_hash

from Billboard import MarshMallow as ma
from flask_marshmallow import Marshmallow

from Billboard.Apps.models import Android_Model
from Billboard.Survey.models import Survey_Model


#many to many relationship between users and surveys
user_survey_table = db.Table ('user_survey_table',
db.Column('user_id', db.Integer, db.ForeignKey('survey_model.id')),
db.Column('survey_id', db.Integer, db.ForeignKey('user_model.id'))
)



class User_Model (db.Model, UserMixin):

    __tablename__ = 'user_model'

    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), unique=True , nullable = False)
    pass_hash = db.Column(db.String(54))
    credit = db.Column (db.Integer)
    role = db.Column (db.String (10) , nullable = False)
    advertised_apps = db.relationship ('Android_Model' , backref = 'user_model' , lazy = True)
    advertised_surveys = db.relationship ('Survey_Model' , backref = 'user_model' , lazy = True)
    submitted_surveys = db.relationship("Survey_Model", secondary = user_survey_table)

    def __init__ (self , name , email , password, role):

        if role in ['user', 'admin']:
            self.name = name
            self.email = email.lower()
            self.pass_hash = generate_password_hash (password)
            self.credit = 2000
            self.role = role

        else:
            raise ValueError()


    def add_and_commit (self):
        db.session.add (self)
        db.session.commit()


    def check_password (self,password):
        return check_password_hash (self.pass_hash,password)


    @staticmethod
    def email_query (req):
        return User_Model.query.filter_by (email = req).first()


    def discharge (self , cost):
        self.credit -= cost
        db.session.commit()

    def charge (self, cost):
        self.credit += cost
        db.session.commit()


    def serialize_one (self):
        return User_Model_Schema().dump(self).data

    @staticmethod
    def serialize_many (arg):
        return User_Model_Schema(many = True).dump (arg).data



class User_Model_Schema (ma.ModelSchema):
    class Meta:
        model = User_Model
        exclude = ('pass_hash','submitted_surveys')
