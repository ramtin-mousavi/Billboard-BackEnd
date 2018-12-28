from Billboard import DataBase as db

from Billboard import MarshMallow as ma
from flask_marshmallow import Marshmallow

from datetime import datetime, timedelta




class Android_Model (db.Model):

    __tablename__ = 'android_model'

    id = db.Column (db.Integer, primary_key = True)
    name =  db.Column(db.String(50), nullable = False)
    package_name = db.Column(db.String(50), nullable = False, unique = True)
    icon = db.Column (db.Text , nullable = False)
    category = db.Column (db.String (30) , nullable = False)
    credit = db.Column (db.Integer)
    count = db.Column (db.Integer)
    download_link = db.Column (db.Text  , nullable = False)
    approval_status = db.Column (db.String(20), nullable = False)
    advertiser_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
    advertise_date = db.Column(db.DateTime)
    expiration_date = db.Column(db.DateTime)


    def __init__ (self, name, package_name, icon, category, credit, dlLink, advertiser_id, duration):

        assert (category in ['Game', 'App'])

        self.name = name.lower()
        self.package_name = package_name.lower()
        self.icon = icon
        self.category = category
        self.credit = credit
        self.count = 0
        self.download_link = dlLink
        self.advertiser_id = advertiser_id
        self.approval_status = 'pending'
        self.advertise_date = datetime.now()
        self.expiration_date = self.advertise_date + timedelta (days = duration)



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

    def expire (self):
        self.approval_status = 'expired'
        db.session.commit()

    def increment_count (self):
        self.count += 1
        db.session.commit()

    def calculate_cost (self):

        duration = (self.advertise_date - self.expiration_date).days
        cost = (20 * duration * self.credit) // ((duration % 10)/1.5)

        return cost



    @staticmethod
    def query_ (status, user = None, filt = None, advertiser_id = None):

        assert (status in ['approved', 'rejected', 'pending', 'all'])

        if user:
            apps_to_show = []

            if filt:
                apps = Android_Model.query.filter_by (category = filt, approval_status = status)
            else:
                apps = Android_Model.query.filter_by (approval_status = status)

            for app in apps:
                if app not in user.installed_android_apps:
                    apps_to_show.append (app)

            return apps_to_show


        if advertiser_id:
            if filt:
                return Android_Model.query.filter_by (category = filt, advertiser_id = advertiser_id)
            return Android_Model.query.filter_by (advertiser_id = advertiser_id)

        if filt:
            return Android_Model.query.filter_by (category = filt, approval_status = status)

        return Android_Model.query.filter_by (approval_status = status)


    #def query_by_package_name (package_name):
    #    return Android_Model.query.filter_by (package_name = package_name).first()


    def serialize_one (self):
        return Android_Model_Schema().dump(self).data

    @staticmethod
    def serialize_many (arg):
        return Android_Model_Schema(many = True).dump (arg).data


class Android_Model_Schema (ma.ModelSchema):
    class Meta:
        model = Android_Model
