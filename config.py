
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from Controlls import Controller


app = Flask(__name__ , static_folder = 'statics')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Ramtin/Desktop/BillBoard Project/DataBase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DataBase = SQLAlchemy(app)



#URLs
app.add_url_rule('/' , view_func = Controller.Home.home)
app.add_url_rule('/signUp' , view_func = Controller.Sign_Up.sign_up , methods = ['POST' , 'GET'])
app.add_url_rule('/login' , view_func = Controller.Login.login , methods = ['POST' , 'GET'])
app.add_url_rule('/logout' , view_func = Controller.Logout.logout)
app.add_url_rule('/profile/<int:pageNum>/' , view_func = Controller.App_Data_Access_Controll.profile_handler)
app.add_url_rule('/giftshop/<int:pageNum>/' , view_func = Controller.Gift_Data_Access_Controll.gift_handler )
app.add_url_rule('/shoppingresult/<int:id>/' , view_func = Controller.Shopping_Handler.shopping_handler )
app.add_url_rule('/addad',view_func=Submit_Ad.add_ad)
app.add_url_rule('/submitadd' , view_func = Controller.Submit_Ad.submit_ad , methods = ['POST' , 'GET'])
app.add_url_rule('/adminpanel' , view_func = Controller.Admin_Panel.admin_panel)
app.add_url_rule('/getPendingRequests/<int:pageNum>' , view_func = Controller.Pending_Requests_Control.get_pending_requests)
app.add_url_rule('/approveorreject/<int:id>' , view_func = Controller.Pending_Requests_Control.approve_or_reject , methods = ['POST' , 'GET'])
app.add_url_rule('/addhistory' , view_func = Controller.Download_History_Manager.add_history , methods = ['POST' , 'GET'])
app.add_url_rule('/getconfirminstalllist/<int:pageNum>' , view_func = Controller.Download_History_Manager.get_confirm_install_list )
app.add_url_rule('/addcredit' , view_func = Controller.Credit_Manager.add_credit , methods = ['POST' , 'GET'])
app.add_url_rule('/revertactions/<appName>' , view_func = Controller.Credit_Manager.revert_actions)
app.add_url_rule('/gifthistory/<int:pageNum>/' , view_func = Controller.Gift_History_Access_Control.gift_history_handler)
app.add_url_rule('/addSurvey' , view_func = Controller.Survey_Manager.add_survey)
app.add_url_rule('/getSurvey' , view_func = Controller.Survey_Manager.get_survey , methods = ['GET','POST'])

# Correct Names
#Correct Survey_Manager












if __name__ == "__main__":

    app.secret_key = os.urandom(12)
    app.run ()
    #app.run(host = '192.168.1.108' , port = 5000, debug = False)
