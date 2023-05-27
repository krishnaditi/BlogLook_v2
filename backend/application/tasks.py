from application.clry import celery
import os
wrkng_dir = os.path.abspath(os.path.dirname(__file__))
path_s = os.path.join(wrkng_dir, "static/")
path_t = os.path.join(wrkng_dir, "templates/")

def format_report(template1,data,User="User"):
    from jinja2 import Template
    with open(template1) as file:
        temp = Template(file.read())
        return temp.render(data=data,User=User)


def pdf_report(d,User):
    from weasyprint import HTML
    msg = format_report(path_t+"monthly_report.html",data=d,User=User)
    html = HTML(string=msg)
    file_name = str(User)+"_Bloglook"+".pdf"
    print(file_name)
    html.write_pdf(target=file_name)


@celery.task()
def export_blog(d, username, email):
    from jinja2 import Template
    import csv
    from application.emailgen import send_email
    with open(path_s+'blog_info_'+username+'.csv', 'w', encoding='utf8', newline='') as f:
        file = csv.DictWriter(f,fieldnames=d[0].keys(),restval='')
        file.writeheader()
        file.writerows(d)
    
    with open(path_t+'user_csv.html','r') as f:
        template = Template(f.read())
    send_email(to_address=email,subject='Exported Blog Details',message=template.render(user=username,data=d),content="html",attachment=path_s+'blog_info_'+username+'.csv')    
    return "Csv created."

@celery.task()
def daily_reminder():
    from jinja2 import Template
    from application.emailgen import send_email
    from application.models import User, Post
    user_details =User.query.all()
   
    for u in user_details :
        email = u.email
        usr = User.query.filter_by(email = u.email).first()
        username = usr.user_name
        
        psts=usr.post
        post_ids=[]
        for i in psts:
            post_ids.append(i.post_id)
        cd=[]
        for i in post_ids:
            parent_list=Post.query.filter_by(post_id=i).first()
        with open(path_t+'daily_reminder.html','r') as f:
            template = Template(f.read())
        send_email(email,'Daily Reminder',template.render(user=username),content="html")

@celery.task()
def monthly_reminder():
    from jinja2 import Template
    from application.emailgen import send_email
    from application.models import User, Post
    user_details =User.query.all()
    user_email_list =[]
    data =[]
    u_list =[]
    
    for u in user_details :
        user_email_list.append(u.email)
        user = User.query.filter_by(email = u.email).first()
        username = user.user_name
        u_list.append(username)
        posts  = user.post
        post_ids = []
        for i in posts:
            post_ids.append(i.post_id)
        
        count=0
        t=[]
        for j in post_ids:
            count+=1    
            l = Post.query.filter_by(post_id=j).first()
            p_heading = l.heading
            p_description = l.description
            p_timestamp = l.timestamp
            
            track_dict = {"SNo":count ,"Heading":p_heading,"Description":p_description, "time_created": p_timestamp}
            t.append(track_dict)
        pdf_report(t,username)

        with open(path_t+'monthly_report.html','r') as f:
            template = Template(f.read())
        send_email(u.email,'Monthly Report',template.render(User=username,data=t),content="html",attachment="./"+str(username)+"_Bloglook.pdf")    
    data.append(t)