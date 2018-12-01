
import os

from Billboard import DataBase as db
from Billboard import app
from Billboard.Authentication.models import User_Model
from Billboard.Apps.models import Android_Model
from Billboard.Gifts.models import Gift_Model
from Billboard.Survey.models import Survey_Model, Question_Model, Item_Model

from flask_script import Manager, prompt_bool


manager = Manager(app)


@manager.command
def initdb():
    user = User_Model ('ادمين' , 'admin','admin','admin')
    user2 = User_Model ('ramtin', 'ramtin@ymail.com' ,'ramtin','admin' )
    db.session.add (user)
    db.session.add (user2)
    db.create_all()
    db.session.commit()





    db.session.add (Android_Model ('Divar','https://parscms.com/my_doc/parscms/article_icon/Divar-logo.png','App',100,'https://play.google.com/store?hl=en','Divar','info@divar.com', '09122222222'))
    db.session.add (Android_Model ('Pelak','https://s.cafebazaar.ir/1/icons/com.example.pelak_512x512.png','App',50,'https://play.google.com/store?hl=en','Pelak','info@pelak.com', '09122222222'))
    db.session.add (Android_Model ('Ding','https://s.cafebazaar.ir/1/icons/com.dinnng.passenger_512x512.png','App',50,'https://play.google.com/store?hl=en','Ding','info@ding.com', '09122222222'))
    db.session.add (Android_Model ('OstadKar','https://s.cafebazaar.ir/1/icons/ir.ostadkar.customer_512x512.png','App',200,'https://play.google.com/store?hl=en','Ostad Kar','info@ostad.com', '09122222222'))
    db.session.add (Android_Model ('Reyhoon','http://daramadinterneti.com/wp-content/uploads/2017/12/reyhoon-logo-300x232.png','App',100,'https://play.google.com/store?hl=en','Reyhoon','info@reyhoon.com', '09123241365'))
    db.session.add (Android_Model ('Digikala','https://is3-ssl.mzstatic.com/image/thumb/Purple122/v4/c4/5e/44/c45e444d-a6c4-bd86-41d7-d3072d6d12df/source/512x512bb.jpg','App',50,'https://play.google.com/store?hl=en','Digikala','info@digikala.com', '09121111111'))
    db.session.add (Android_Model ('CinemaTicket','https://avvalmarket.ir/apps/com.hampardaz.cinematicket/icon/512x512.png','App',50,'https://play.google.com/store?hl=en','Cinema Ticket','info@cinema.com', '09123241365'))
    db.session.add (Android_Model ('Snapp','https://getandroid.ir/uploads/posts/2017-03/1488433149_Snapp-icon.png','App',200,'https://play.google.com/store?hl=en','Snapp','info@snapp.com', '09122222222'))
    db.session.add (Android_Model ('SoccerStars','https://images-eu.ssl-images-amazon.com/images/I/91pslkY9oiL.png','Game',100,'https://play.google.com/store?hl=en','Soccer Company','info@soccer.com', '09122222222'))
    db.session.add (Android_Model ('Loop','https://is3-ssl.mzstatic.com/image/thumb/Purple115/v4/d2/3f/90/d23f906c-f0b8-90bb-d52e-1a46604e413e/AppIcon-1x_U007emarketing-85-220-8.jpeg/246x0w.jpg','Game',100,'https://play.google.com/store?hl=en','Loop Game','info@loop.com', '09122222222'))
    db.session.add (Android_Model ('Tap30','https://s.cafebazaar.ir/1/icons/taxi.tap30.driver_512x512.png','App',150,'https://play.google.com/store?hl=en','Tap30','Tap30@yahoo.com', '09123333333'))



    db.session.add (Gift_Model ('Gift Card' , 'giftcard.jpg' , '0000' , '1$' , 5 , 50))
    db.session.add (Gift_Model ('Gift Card' , 'giftcard.jpg' , '1111' , '2$' , 4 , 100))
    db.session.add (Gift_Model ('Gift Card' , 'giftcard.jpg' , '2222' , '3$' , 3 , 150))
    db.session.add (Gift_Model ('Gift Card' , 'giftcard.jpg' , '3333' , '4$' , 2 , 200))
    db.session.add (Gift_Model ('Gift Card' , 'giftcard.jpg' , '4444' , '5$' , 2 , 250))
    db.session.add (Gift_Model ('Gift Card' , 'giftcard.jpg' , '5555' , '6$' , 2 , 300))
    db.session.add (Gift_Model ('Gift Card' , 'giftcard.jpg' , '6666' , '7$' , 2 , 350))
    db.session.add (Gift_Model ('Gift Card' , 'giftcard.jpg' , '7777' , '8$' , 1 , 400))
    db.session.add (Gift_Model ('Gift Card' , 'giftcard.jpg' , '8888' , '9$' , 1 , 450))
    db.session.add (Gift_Model ('Gift Card' , 'giftcard.jpg' , '9999' , '10$' , 1 , 500))



    survey = Survey_Model ('survey1','description1')
    db.session.add (survey)
    db.session.commit()

    question1 = Question_Model ('qestion1', survey.id)
    question2 = Question_Model ('qestion2', survey.id)
    question3 = Question_Model ('qestion3', survey.id)
    db.session.add_all ([question1,question2,question3])
    db.session.commit()


    item1 = Item_Model ('item1-question1', question1.id)
    item2 = Item_Model ('item2-question1', question1.id)
    item3 = Item_Model ('item3-question1', question1.id)
    item4 = Item_Model ('item1-question2', question2.id)
    item5 = Item_Model ('item2-question2', question2.id)
    item6 = Item_Model ('item1-question3', question3.id)
    item7 = Item_Model ('item2-question3', question3.id)
    item8 = Item_Model ('item3-question3', question3.id)
    item9 = Item_Model ('item4-question3', question3.id)
    db.session.add_all([item9,item8,item7,item1,item2,item6,item3,item4,item5])
    db.session.commit()


    survey2 = Survey_Model ('survey2','description2')
    db.session.add (survey2)
    db.session.commit()


    question21 = Question_Model ('qestion21', survey2.id)
    question22 = Question_Model ('qestion22', survey2.id)
    question23 = Question_Model ('qestion23', survey2.id)

    db.session.add_all ([question21,question22,question23])
    db.session.commit()


    item21 = Item_Model ('item1-question21', question21.id)
    item22 = Item_Model ('item2-question21', question21.id)
    item23 = Item_Model ('item3-question21', question21.id)
    item24 = Item_Model ('item1-question22', question22.id)
    item25 = Item_Model ('item2-question22', question22.id)
    item26 = Item_Model ('item1-question23', question23.id)
    item27 = Item_Model ('item2-question23', question23.id)
    item28 = Item_Model ('item3-question23', question23.id)
    item29 = Item_Model ('item4-question23', question23.id)

    db.session.add_all ([item21,item22,item23,item24,item25,item26,item27,item28,item29])
    db.session.commit()



    for app in Android_Model.query.all():
        app.approve()
    for survey in Survey_Model.query.all():
        survey.approve()

    print ('Initialized the database')


@manager.command
def dropdb():
    if prompt_bool(
        "Are you sure you want to lose all your data"):
        db.drop_all()
        print ('Dropped the database')


@manager.command
def run():
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0')

if __name__ == '__main__':
    manager.run()
