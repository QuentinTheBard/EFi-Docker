from enum import unique
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_migrate import Migrate
from datetime import datetime
# from myblog import db
import os
app = Flask(__name__)

MYSQL_HOST = os.environ.get('MYSQL_HOST', '143.198.156.171') 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://BD2021:BD2021itec@'+MYSQL_HOST+'/blog_python'
app.config["SECRET_KEY"] = "acalepongoloquequiera"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["pydev_do_not_trace"] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, author, title, body) -> None:
        self.author = author
        self.title = title
        self.body = body

    def __repr__(self) -> str:
        return f'Post: {self.title}'
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.Text)

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

    def __repr__(self) -> str:
        return f'User: {self.username}'

if __name__=='__main__':
    # app.run(debug=True)
    app.run(debug=True,host='0.0.0.0', port=8000)
    # app.run(host='0.0.0.0', port=8000)