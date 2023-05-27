from flask import Flask
from flask_security import SQLAlchemyUserDatastore, Security,hash_password
from application.models import db, User, Role
from application.api import UserAPI, BlogAPI, SearchAPI, FollowerAPI, EngagementAPI, ExportBlogAPI, OtherUserAPI
from flask_restful import Api
import os
from flask_cors import CORS
from celery.schedules import crontab
import application.clry as clry
from application.cache import cache
from application.tasks import daily_reminder, monthly_reminder

app = Flask(__name__)
app.secret_key = "thisisasecertkey"
app.config['WTF_CSRF_ENABLED'] = False
current_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(current_dir, "project.sqlite3")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_PASSWORD_SALT'] = 'thisisasecretsalt'
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authentication-Token'


api=Api(app)
CORS(app)
db.init_app(app)
cache.init_app(app)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

celery = clry.celery
app.app_context().push()

celery.conf.update(
     broker_url='redis://localhost:6379/1',
     result_backend='redis://localhost:6379/2'
 )

celery.Task = clry.ContextTask
app.app_context().push()

api.add_resource(UserAPI,"/api/user","/api/user/<string:email>")
api.add_resource(BlogAPI, "/api/blog/<string:email>", "/api/blog/<string:email>/<int:post_id>")
api.add_resource(FollowerAPI, "/api/followaction/<string:email>", "/api/followaction/<string:email>/<int:profile_id>")
api.add_resource(SearchAPI, "/api/search/<string:email>/<string:sea>")
api.add_resource(EngagementAPI, "/api/engagement/<string:email>")
api.add_resource(ExportBlogAPI, "/api/export/<string:email>")
api.add_resource(OtherUserAPI, "/api/userprofile/<string:email>/<int:profile_id>")

@app.before_first_request
def create_tables():
    db.create_all()

@app.before_first_request
def create_user():
    if not user_datastore.find_user(email="krishnaanushka137@gmail.com"):
        user_datastore.create_user(email="krishnaanushka137@gmail.com",user_name="Anushka",full_name='Ak', password=hash_password("password"))
    db.session.commit()  

import datetime
import pytz
def timee(): 
    return datetime.datetime.now(pytz.timezone('Asia/Kolkata')) 


@celery.on_after_finalize.connect
def monthly_report(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=20, minute=15, day_of_month="9", nowfun=timee),
        monthly_reminder.s(),
    )
    sender.add_periodic_task(
        crontab(hour=20, minute=17, day_of_week='*', nowfun=timee),
        daily_reminder.s(),
    )

celery.conf.timezone = 'Asia/Kolkata'

if __name__=='__main__':
    app.run(debug=True)
#redis-server desktop
#npm run serve in frntend
#python3 app.py in bkend
#MailHog
#celery -A app.celery beat --max-interval 1 -l info in bkend
#celery -A app.celery worker -l info in bkend 1st
