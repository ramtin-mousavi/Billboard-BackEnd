from Billboard import DataBase as db

from Billboard import MarshMallow as ma
from flask_marshmallow import Marshmallow

from datetime import datetime, timedelta




class Android_Model (db.Model):

    __tablename__ = 'android_model'

    id = db.Column (db.Integer, primary_key = True)
    name =  db.Column(db.String(50), nullable = False)
    icon = db.Column (db.Text , nullable = False)
    category = db.Column (db.String (30) , nullable = False)
    credit = db.Column (db.Integer)
    count = db.Column (db.Integer)
    download_link = db.Column (db.Text  , nullable = False)
    approval_status = db.Column (db.String(20), nullable = False)
    advertiser_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
    advertise_date = db.Column(db.DateTime)
    expiration_date = db.Column(db.DateTime)


    #valid_approvals = ['approved','rejected','pending']
    valid_categories = ['Game' , 'App']


    def __init__ (self, name, icon, category, credit, dlLink, advertiser_id, duration):

        if category in Android_Model.valid_categories:

            self.name = name.lower()
            self.icon = icon
            self.category = category
            self.credit = credit
            self.count = 0
            self.download_link = dlLink
            self.advertiser_id = advertiser_id
            self.approval_status = 'pending'
            self.advertise_date = datetime.now()
            self.expiration_date = self.advertise_date + timedelta (days = duration)

        else:
            raise ValueError()

    def charge (self,count):
        self.count += count
        db.session.commit()

    def add_and_commit (self):
        db.session.add(self)
        db.session.commit()

    def approve (self):
        self.approval_status = 'approved'
        db.session.commit()

    def reject (self):
        self.approval_status = 'rejected'
        db.session.commit()


    @staticmethod
    def query_ (status, filt = None, advertiser_id = None):

        assert (status in ['approved', 'rejected', 'pending', 'all'])

        if advertiser_id:
            if filt:
                return Android_Model.query.filter_by (category = filt, advertiser_id = advertiser_id)
            return Android_Model.query.filter_by (advertiser_id = advertiser_id)

        if filt:
            return Android_Model.query.filter_by (category = filt, approval_status = status)

        return Android_Model.query.filter_by (approval_status = status)




    def serialize_one (self):
        return Android_Model_Schema().dump(self).data

    @staticmethod
    def serialize_many (arg):
        return Android_Model_Schema(many = True).dump (arg).data


class Android_Model_Schema (ma.ModelSchema):
    class Meta:
        model = Android_Model
