from Billboard import DataBase as db

from Billboard import MarshMallow as ma
from flask_marshmallow import Marshmallow




class Android_Model (db.Model):
    id = db.Column (db.Integer, primary_key = True)
    name =  db.Column(db.String(50), nullable = False)
    icon = db.Column (db.Text , nullable = False)
    category = db.Column (db.String (30) , nullable = False)
    credit = db.Column (db.Integer)
    count = db.Column (db.Integer)
    download_link = db.Column (db.Text  , nullable = False)
    company = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), nullable = False)
    phone = db.Column(db.String(50), nullable = False)
    is_approved = db.Column (db.Boolean , nullable = False)
    valid_categories = ['Game' , 'App']


    def __init__ (self, name, icon, category , credit , dlLink, company, email,phone):

        if category in Android_Model.valid_categories:

            self.name = name.lower()
            self.icon = icon
            self.category = category
            self.credit = credit
            self.count = 0
            self.download_link = dlLink
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
    def all_query ():
        return Android_Model.query.filter (Android_Model.is_approved == True)

    @staticmethod
    def filter_query (fil):
        return Android_Model.query.filter_by (category = fil , is_approved = True)


    @staticmethod
    def query_for_admin ():
        return Android_Model.query.filter (Android_Model.is_approved == False)


    def serialize_one (self):
        return Android_Model_Schema().dump(self).data

    @staticmethod
    def serialize_many (arg):
        return Android_Model_Schema(many = True).dump (arg).data


class Android_Model_Schema (ma.ModelSchema):
    class Meta:
        model = Android_Model
        exclude = ('is_approved',)
