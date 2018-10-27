# cd ..
import sys
sys.path.append("..")

#import DataBase
from config import DataBase as db
from flask_login import UserMixin
from werkzeug import generate_password_hash, check_password_hash



class User_Model (db.Model, UserMixin):
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



class Gift_Model (myDB.Model):
    id = myDB.Column (myDB.Integer, primary_key = True)
    name =  myDB.Column(myDB.String(50), nullable = False)
    icon = myDB.Column (myDB.Text , nullable = False)
    code = myDB.Column (myDB.Integer)
    description = myDB.Column (myDB.Text , nullable = False)
    supply = myDB.Column (myDB.Integer)
    cost = myDB.Column (myDB.Integer)



    def __init__ (self,name,icon,code,description , supply, cost):
        self.name = name
        self.icon = icon
        self.description = description
        self.supply = supply
        self.cost = cost
        self.code = code



    def discharge (self):
        if self.supply > 0 :
            self.supply -= 1
            myDB.session.commit()

    def charge (self, count):
        self.supply += count
        myDB.session.commit()


    @staticmethod
    def paginate_query (per,num,error):
        return Gift_Model.query.filter(Gift_Model.supply > 0).paginate (per_page = per , page = num , error_out = error)

    @staticmethod
    def id_query (ID):
        return Gift_Model.query.get (ID)

    #####date = myDB.Column(myDB.DateTime, default = datetime.now)





class Survey_Model (myDB.Model):

    id = myDB.Column(myDB.Integer, primary_key = True)
    title = myDB.Column (myDB.String(40), nullable = False)
    description = myDB.Column (myDB.Text , nullable = False)
    # foreign key to user
    questions = myDB.relationship ('Question_Model' , backref = 'survey_model' , lazy = True)
    is_approved = myDB.Column (myDB.Boolean , nullable = False)


    def __init__ (self , title , description ):
        self.title = title
        self.description = description
        self.is_approved = False



    def approve (self):
        self.is_approved = True
        myDB.session.commit()

    def reject (self):
        myDB.session.delete (self)
        myDB.session.commit()

    def add_and_commit (self):
        myDB.session.add (self)
        myDB.session.commit()



class Question_Model (myDB.Model):

    id = myDB.Column(myDB.Integer, primary_key = True)
    context = myDB.Column (myDB.Text , nullable = False)
    items = myDB.relationship ('Item_Model' , backref = 'question_model' , lazy = True)
    survey_id = myDB.Column(myDB.Integer, myDB.ForeignKey('survey_model.id'), nullable=False)

    def __init__ (self , context , survey_id):
        self.context = context
        self.survey_id = survey_id


    def add_and_commit (self):
        myDB.session.add (self)
        myDB.session.commit()


class Item_Model (myDB.Model):

    id = myDB.Column(myDB.Integer, primary_key = True)
    context = myDB.Column (myDB.Text , nullable = False)
    question_id = myDB.Column(myDB.Integer, myDB.ForeignKey('question_model.id'), nullable=False)

    def __init__ (self , context , question_id):
        self.context = context
        self.question_id = question_id


    def add_and_commit (self):
        myDB.session.add (self)
        myDB.session.commit()
