from flask_security import UserMixin, RoleMixin
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Follow(db.Model):
    __tablename__ = "follows"
    user_id = db.Column(db.String, db.ForeignKey("user.user_name"), primary_key=True)#mera id
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.profile_id"), primary_key=True)#ham jisko follow krte uska id 

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class User(db.Model, UserMixin): 
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(60), unique = True, nullable = False)
    full_name = db.Column(db.String(100), nullable = False)
    user_name = db.Column(db.String(60), unique = True, nullable = False)
    password = db.Column(db.String(100), nullable = False)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False) 
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('User', lazy='dynamic'))
    profile = db.relationship("Profile", backref=db.backref('User'))
    post = db.relationship("Post", backref=db.backref('User'))

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))    


class Profile(db.Model):
    __tablename__ = "profile"
    profile_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    about = db.Column(db.String(200))
    profile_pic = db.Column(db.String) 
    total_post = db.Column(db.Integer)
    user_id = db.Column(db.String, db.ForeignKey("user.user_name"), unique=True)


class Post(db.Model):
    __tablename__ = "post"
    post_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_name"))
    image = db.Column(db.String)
    heading = db.Column(db.String, nullable = False)
    description = db.Column(db.String)
    timestamp=db.Column(db.DateTime, default=datetime.datetime.utcnow)


      

