from Billboard import DataBase as db

from Billboard.Authentication.models import User_Model
from Billboard.Apps.models import Android_Model
from Billboard.Gifts.models import Gift_Model
from Billboard.Survey.models import Survey_Model, Question_Model, Item_Model

def make_instances ():

    user = User_Model ('ادمين' , 'admin','admin','admin')
    user2 = User_Model ('ramtin', 'ramtin@ymail.com' ,'ramtin','admin' )
    db.session.add (user)
    db.session.add (user2)
    db.session.commit()

    db.session.add (Android_Model ('Divar','package_name1','https://parscms.com/my_doc/parscms/article_icon/Divar-logo.png','App',100,'https://play.google.com/store?hl=en',1,30))
    db.session.add (Android_Model ('Pelak','package_name2','https://s.cafebazaar.ir/1/icons/com.example.pelak_512x512.png','App',50,'https://play.google.com/store?hl=en',1,30))
    db.session.add (Android_Model ('Ding','package_name3','https://s.cafebazaar.ir/1/icons/com.dinnng.passenger_512x512.png','App',50,'https://play.google.com/store?hl=en',1,30))
    db.session.add (Android_Model ('OstadKar','package_name4','https://s.cafebazaar.ir/1/icons/ir.ostadkar.customer_512x512.png','App',200,'https://play.google.com/store?hl=en',1,30))
    db.session.add (Android_Model ('Reyhoon','package_name5','http://daramadinterneti.com/wp-content/uploads/2017/12/reyhoon-logo-300x232.png','App',100,'https://play.google.com/store?hl=en',1,30))
    db.session.add (Android_Model ('Digikala','package_name6','https://is3-ssl.mzstatic.com/image/thumb/Purple122/v4/c4/5e/44/c45e444d-a6c4-bd86-41d7-d3072d6d12df/source/512x512bb.jpg','App',50,'https://play.google.com/store?hl=en',2,30))
    db.session.add (Android_Model ('CinemaTicket','package_name7','https://avvalmarket.ir/apps/com.hampardaz.cinematicket/icon/512x512.png','App',50,'https://play.google.com/store?hl=en',2,30))
    db.session.add (Android_Model ('Snapp','package_name8','https://getandroid.ir/uploads/posts/2017-03/1488433149_Snapp-icon.png','App',200,'https://play.google.com/store?hl=en',2,30))
    db.session.add (Android_Model ('SoccerStars','package_name9','https://images-eu.ssl-images-amazon.com/images/I/91pslkY9oiL.png','Game',100,'https://play.google.com/store?hl=en',2,30))
    db.session.add (Android_Model ('Loop','package_name10','https://is3-ssl.mzstatic.com/image/thumb/Purple115/v4/d2/3f/90/d23f906c-f0b8-90bb-d52e-1a46604e413e/AppIcon-1x_U007emarketing-85-220-8.jpeg/246x0w.jpg','Game',100,'https://play.google.com/store?hl=en',2,30))
    db.session.add (Android_Model ('Tap30','package_name11','https://s.cafebazaar.ir/1/icons/taxi.tap30.driver_512x512.png','App',150,'https://play.google.com/store?hl=en',2,30))
    db.session.commit()

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
    db.session.commit()

    survey = Survey_Model ('نظر سنجی شماره یک','توضیحات نظرسنجی شماره یک',1,30,100)
    survey2 = Survey_Model ('نظر سنجی شماره دو','توضیحات نظر سنجی شماره دو',2,30,200)
    db.session.add (survey)
    db.session.add (survey2)
    db.session.commit()

    question1 = Question_Model ('سوال اول', survey.id)
    question2 = Question_Model ('سوال دوم', survey.id)
    question3 = Question_Model ('سوال سوم', survey.id)
    db.session.add_all ([question1,question2,question3])
    db.session.commit()

    question21 = Question_Model ('سوال اول', survey2.id)
    question22 = Question_Model ('سوال دوم', survey2.id)
    question23 = Question_Model ('سوال سوم', survey2.id)
    db.session.add_all ([question21,question22,question23])
    db.session.commit()

    item1 = Item_Model ('آیتم اول سوال اول', question1.id)
    item2 = Item_Model ('آیتم دوم سوال اول', question1.id)
    item3 = Item_Model ('آیتم سوم سوال اول', question1.id)
    item4 = Item_Model ('آیتم اول سوال دوم', question2.id)
    item5 = Item_Model ('آیتم دوم سوال دوم', question2.id)
    item6 = Item_Model ('آیتم اول سوال سوم', question3.id)
    item7 = Item_Model ('آیتم دوم سوال سوم', question3.id)
    item8 = Item_Model ('آیتم سوم سوال سوم', question3.id)
    item9 = Item_Model ('آیتم چهارم سوال سوم', question3.id)
    db.session.add_all([item9,item8,item7,item1,item2,item6,item3,item4,item5])
    db.session.commit()

    item21 = Item_Model ('آیتم اول سوال اول', question21.id)
    item22 = Item_Model ('آیتم دوم سوال اول', question21.id)
    item23 = Item_Model ('آیتم سوم سوال اول', question21.id)
    item24 = Item_Model ('آیتم اول سوال دوم', question22.id)
    item25 = Item_Model ('آیتم دوم سوال دوم', question22.id)
    item26 = Item_Model ('آیتم اول سوال سوم', question23.id)
    item27 = Item_Model ('آیتم دوم سوال سوم', question23.id)
    item28 = Item_Model ('آیتم سوم سوال سوم', question23.id)
    item29 = Item_Model ('آیتم چهارم سوال سوم', question23.id)
    db.session.add_all ([item21,item22,item23,item24,item25,item26,item27,item28,item29])
    db.session.commit()

    for app in Android_Model.query.all():
        app.approve()
    for survey in Survey_Model.query.all():
        survey.approve()
