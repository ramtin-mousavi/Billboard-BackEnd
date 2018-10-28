 # cd ..
import sys
sys.path.append("..")

from Models import Model
from Controller import app
from Controller import DataBase as db
from flask_script import Manager, prompt_bool

manager = Manager(app)

@manager.command
def initdb():
    user = Model.User_Model ('ادمين' , 'admin','admin')
    db.session.add (user)
    db.create_all()
    db.session.commit()

    #db.session.add (Model.Android_Model ('Chrome','chrome.png','App',50,'https://play.google.com/store?hl=en','http://192.168.1.108/revertactions/chrome','company','email', 'phone'))




    db.session.add (Model.Android_Model ('Divar','https://parscms.com/my_doc/parscms/article_icon/Divar-logo.png','App',100,'https://play.google.com/store?hl=en','http://192.168.1.108:5000/revertactions/divar','Divar','info@divar.com', '09122222222'))
    db.session.add (Model.Android_Model ('Pelak','https://s.cafebazaar.ir/1/icons/com.example.pelak_512x512.png','App',50,'https://play.google.com/store?hl=en','http://192.168.1.108:5000/revertactions/pelak','Pelak','info@pelak.com', '09122222222'))
    db.session.add (Model.Android_Model ('Ding','https://s.cafebazaar.ir/1/icons/com.dinnng.passenger_512x512.png','App',50,'https://play.google.com/store?hl=en','http://192.168.1.108:5000/revertactions/ding','Ding','info@ding.com', '09122222222'))
    db.session.add (Model.Android_Model ('OstadKar','https://s.cafebazaar.ir/1/icons/ir.ostadkar.customer_512x512.png','App',200,'https://play.google.com/store?hl=en','http://192.168.1.108:5000/revertactions/ostadkar','Ostad Kar','info@ostad.com', '09122222222'))
    db.session.add (Model.Android_Model ('Reyhoon','http://daramadinterneti.com/wp-content/uploads/2017/12/reyhoon-logo-300x232.png','App',100,'https://play.google.com/store?hl=en','http://192.168.1.108:5000/revertactions/reyhoon','Reyhoon','info@reyhoon.com', '09123241365'))
    db.session.add (Model.Android_Model ('Digikala','https://is3-ssl.mzstatic.com/image/thumb/Purple122/v4/c4/5e/44/c45e444d-a6c4-bd86-41d7-d3072d6d12df/source/512x512bb.jpg','App',50,'https://play.google.com/store?hl=en','http://192.168.1.108:5000/revertactions/digikala','Digikala','info@digikala.com', '09121111111'))

    db.session.add (Model.Android_Model ('CinemaTicket','https://avvalmarket.ir/apps/com.hampardaz.cinematicket/icon/512x512.png','App',50,'https://play.google.com/store?hl=en','http://192.168.1.108:5000/revertactions/cinematicket','Cinema Ticket','info@cinema.com', '09123241365'))
    #db.session.add (Model.Android_Model ('Facebook2','facebook.png','App',50,'https://play.google.com/store?hl=en','https://google.com'))
    #db.session.add (Model.Android_Model ('Instagram2','instagram.png','App',50,'https://play.google.com/store?hl=en','https://google.com'))
    db.session.add (Model.Android_Model ('Snapp','https://getandroid.ir/uploads/posts/2017-03/1488433149_Snapp-icon.png','App',200,'https://play.google.com/store?hl=en','http://192.168.1.108:5000/revertactions/snapp','Snapp','info@snapp.com', '09122222222'))
    #db.session.add (Model.Android_Model ('Tap30-2','tap30.png','App',300,'https://play.google.com/store?hl=en','https://google.com'))
    #db.session.add (Model.Android_Model ('Telegram2','telegram.png','App',100,'https://play.google.com/store?hl=en','https://google.com'))
    #db.session.add (Model.Android_Model ('Twitter2','twitter.png','App',50,'https://play.google.com/store?hl=en','https://google.com'))
    #db.session.add (Model.Android_Model ('Whatsapp2','whatsapp.png','App',50,'https://play.google.com/store?hl=en','https://google.com'))
    db.session.add (Model.Android_Model ('SoccerStars','https://images-eu.ssl-images-amazon.com/images/I/91pslkY9oiL.png','Game',100,'https://play.google.com/store?hl=en','http://192.168.1.108:5000/revertactions/soccerstars','Soccer Company','info@soccer.com', '09122222222'))
    #db.session.add (Model.Android_Model ('Facebook3','facebook.png','App',50,'https://play.google.com/store?hl=en','https://google.com'))
    #db.session.add (Model.Android_Model ('Instagram3','instagram.png','App',50,'https://play.google.com/store?hl=en','https://google.com'))
    #db.session.add (Model.Android_Model ('Snapp3','snapp.png','App',200,'https://play.google.com/store?hl=en','https://google.com'))
    #db.session.add (Model.Android_Model ('Tap30-3','tap30.png','App',300,'https://play.google.com/store?hl=en','https://google.com'))
    #db.session.add (Model.Android_Model ('Telegram3','telegram.png','App',100,'https://play.google.com/store?hl=en','https://google.com'))
    #db.session.add (Model.Android_Model ('Twitter3','twitter.png','App',50,'https://play.google.com/store?hl=en','https://google.com'))
    #db.session.add (Model.Android_Model ('Whatsapp3','whatsapp.png','App',50,'https://play.google.com/store?hl=en','https://google.com'))
    #db.session.add (Model.Android_Model ('Soccer Stars2','soccerstar.jpg','Game',100,'https://play.google.com/store?hl=en','https://google.com'))
    db.session.add (Model.Android_Model ('Loop','https://is3-ssl.mzstatic.com/image/thumb/Purple115/v4/d2/3f/90/d23f906c-f0b8-90bb-d52e-1a46604e413e/AppIcon-1x_U007emarketing-85-220-8.jpeg/246x0w.jpg','Game',100,'https://play.google.com/store?hl=en','http://192.168.1.108:5000/revertactions/loop','Loop Game','info@loop.com', '09122222222'))



    db.session.add (Model.Android_Model ('Tap30','https://s.cafebazaar.ir/1/icons/taxi.tap30.driver_512x512.png','App',150,'https://play.google.com/store?hl=en','http://192.168.1.108/revertactions/tap30','Tap30','Tap30@yahoo.com', '09123333333'))




    #db.session.add (IosModel ('Ios Game','iosgame.png','Game',500,'https://play.google.com/store?hl=en','http://192.168.43.216:5000/checkinstall/iosgame','company','email', 'phone'))
    #db.session.add (IosModel ('Ios App','iosapp.png','App',1000,'https://play.google.com/store?hl=en','http://192.168.43.216:5000/checkinstall/iosapp','company','email', 'phone'))

    db.session.add (Model.Gift_Model ('Gift Card' , 'giftcard.jpg' , 0000 , '1$' , 5 , 50))
    db.session.add (Model.Gift_Model ('Gift Card' , 'giftcard.jpg' , 1111 , '2$' , 4 , 100))
    db.session.add (Model.Gift_Model ('Gift Card' , 'giftcard.jpg' , 2222 , '3$' , 3 , 150))
    db.session.add (Model.Gift_Model ('Gift Card' , 'giftcard.jpg' , 3333 , '4$' , 2 , 200))
    db.session.add (Model.Gift_Model ('Gift Card' , 'giftcard.jpg' , 4444 , '5$' , 2 , 250))
    db.session.add (Model.Gift_Model ('Gift Card' , 'giftcard.jpg' , 5555 , '6$' , 2 , 300))
    db.session.add (Model.Gift_Model ('Gift Card' , 'giftcard.jpg' , 6666 , '7$' , 2 , 350))
    db.session.add (Model.Gift_Model ('Gift Card' , 'giftcard.jpg' , 7777 , '8$' , 1 , 400))
    db.session.add (Model.Gift_Model ('Gift Card' , 'giftcard.jpg' , 8888 , '9$' , 1 , 450))
    db.session.add (Model.Gift_Model ('Gift Card' , 'giftcard.jpg' , 9999 , '10$' , 1 , 500))

    db.session.commit()

    for app in Model.Android_Model.query.all():
        app.approve()
    #for item in IosModel.query.all():
        #item.approve()

    print ('Initialized the database')

@manager.command
def dropdb():
    if prompt_bool(
        "Are you sure you want to lose all your data"):
        db.drop_all()
        print ('Dropped the database')

if __name__ == '__main__':
    manager.run()
