 # cd ..
import sys
sys.path.append("..")

#import DataBase
from Controller import DataBase as db
from flask_login import UserMixin
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime


class User_Model (db.Model, UserMixin):

    __tablename__ = 'user_model'

    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), unique=True , nullable = False)
    pass_hash = db.Column(db.String(54))
    credit = db.Column (db.Integer)


    def __init__ (self , name , email , password):
        self.name = name
        self.email = email.lower()
        self.pass_hash = generate_password_hash (password)
        self.credit = 2000


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

    def serialize(self):
        return {
            "name": self.name,
            "email": self.email,
            "credit": self.credit
        }



class Android_Model (db.Model):
    id = db.Column (db.Integer, primary_key = True)
    name =  db.Column(db.String(50), nullable = False)
    icon = db.Column (db.Text , nullable = False)
    category = db.Column (db.String (30) , nullable = False)
    credit = db.Column (db.Integer)
    count = db.Column (db.Integer)
    download_link = db.Column (db.Text  , nullable = False)
    deepLink = db.Column (db.Text , nullable = False)
    company = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), nullable = False)
    phone = db.Column(db.String(50), nullable = False)
    is_approved = db.Column (db.Boolean , nullable = False)
    valid_categories = ['Game' , 'App']


    def __init__ (self, name, icon, category , credit , dlLink, deepLink, company, email,phone):

        if category in Android_Model.valid_categories:

            self.name = name.lower()
            self.icon = icon
            self.category = category
            self.credit = credit
            self.count = 0
            self.download_link = dlLink
            self.deepLink = deepLink
            self.company = company
            self.phone = phone
            self.email = email
            self.is_approved = False

        else:
            raise ValueError()

    def charge (self,count):
        self.count += count
        db.session.commit()

    def add_and_commit (self):
        db.session.add(self)
        db.session.commit()

    def approve (self):
        self.is_approved = True
        db.session.commit()

    def reject (self):
        db.session.delete (self)
        db.session.commit()


    @staticmethod
    def paginate_query (per,num,error):
        return Android_Model.query.filter(Android_Model.is_approved == True).paginate (per_page = per , page = num , error_out = error)

    @staticmethod
    def all_query ():
        return Android_Model.query.filter (Android_Model.is_approved == True)

    @staticmethod
    def paginate_by_filter (per,num,error, fil):
        return Android_Model.query.filter_by (category = fil , is_approved = True).paginate (per_page = per , page = num , error_out = error)

    @staticmethod
    def filter_query (fil):
        return Android_Model.query.filter_by (category = fil , is_approved = True)

    @staticmethod
    def paginate_query_for_admin (per,num,error):
        return Android_Model.query.filter (Android_Model.is_approved == False).paginate (per_page = per , page = num , error_out = error)



class Gift_Model (db.Model):
    id = db.Column (db.Integer, primary_key = True)
    name =  db.Column(db.String(50), nullable = False)
    icon = db.Column (db.Text , nullable = False)
    code = db.Column (db.Integer)
    description = db.Column (db.Text , nullable = False)
    supply = db.Column (db.Integer)
    cost = db.Column (db.Integer)




    def __init__ (self,name,icon,code,description , supply, cost , user_id = None):
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



    @staticmethod
    def paginate_query (per,num,error):
        return Gift_Model.query.filter(Gift_Model.supply > 0).paginate (per_page = per , page = num , error_out = error)

    @staticmethod
    def id_query (Id):
        return Gift_Model.query.get (Id)




class Gift_History_Model (db.Model):

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, nullable = False)
    gift_id = db.Column(db.Integer, nullable = False)
    date = db.Column(db.DateTime, default = datetime.now)
    description = db.Column(db.Text, nullable=False)
    code = db.Column(db.Integer)


    def __init__(self, user_id , giftId ):
        self.user_id = user_id
        self.gift_id = giftId
        self.description = Gift_Model.query.get (giftId).description
        self.code = Gift_Model.query.get (giftId).code


    def add_and_commit(self):
        db.session.add (self)
        db.session.commit()


    @staticmethod
    def paginate_query(per, num, error, user_id):
        return Gift_History_Model.query.filter_by(user_id = user_id).paginate(per_page=per, page=num, error_out=error)




class Survey_Model (db.Model):

    __tablename__ = 'survey_model'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column (db.String(40), nullable = False)
    description = db.Column (db.Text , nullable = False)
    # foreign key to user
    questions = db.relationship ('Question_Model' , backref = 'survey_model' , lazy = True)
    is_approved = db.Column (db.Boolean , nullable = False)
    credit = db.Column (db.Integer , nullable = False)


    def __init__ (self , title , description ):
        self.title = title
        self.description = description
        self.is_approved = True
        self.credit = 100



    def approve (self):
        self.is_approved = True
        db.session.commit()

    def reject (self):
        db.session.delete (self)
        db.session.commit()

    def add_and_commit (self):
        db.session.add (self)
        db.session.commit()


    @staticmethod
    def paginate_query (per,num,error):
        return Survey_Model.query.filter(Survey_Model.is_approved == True).paginate (per_page = per , page = num , error_out = error)



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
