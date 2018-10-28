

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__ , static_folder = 'statics' , template_folder = 'Views')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Ramtin/Desktop/BillBoard Project/DataBase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DataBase = SQLAlchemy(app)
















if __name__ == "__main__":

    app.secret_key = os.urandom(12)
    app.run ()
    #app.run(host = '192.168.1.108' , port = 5000, debug = False)
