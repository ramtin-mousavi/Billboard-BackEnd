import schedule
import time
import datetime

from Billboard.Survey.models import Survey_Model
from Billboard.Apps.models import Android_Model


class Schedule:

    @staticmethod
    def run_schedule():
        schedule.every().day.at("00:00").do(Schedule.expire_apps)
        schedule.every().day.at("00:00").do(Schedule.expire_surveys)
        while True:
            schedule.run_pending()
            time.sleep(60)

    @staticmethod
    def expire_apps ():
        present = datetime.datetime.now()

        for app in Android_Model.query_ ('approved'):
            if present > app.expiration_date:
                app.expire()

    @staticmethod
    def expire_surveys ():
        present = datetime.datetime.now()

        for survey in Survey_Model.query_ ('approved'):
            if present > survey.expiration_date:
                survey.expire()
