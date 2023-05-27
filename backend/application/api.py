from flask import Flask, request
from flask_restful import Resource, reqparse, fields, marshal_with, Api
from application.models import db, User as user_model, Role, Profile, Post, Follow
import datetime
from flask_security import auth_required, current_user, hash_password, SQLAlchemyUserDatastore, Security, login_required
from flask import jsonify
import os
import werkzeug
import base64
import application.tasks as tasks
from application.cache import cache
from werkzeug.utils import secure_filename

wrkng_dir = os.path.abspath(os.path.dirname(__file__))

user_datastore = SQLAlchemyUserDatastore(db, user_model, Role)
security = Security(user_datastore)
import matplotlib.pyplot as plt
figure = plt.figure()

user_req_args = reqparse.RequestParser()
user_req_args.add_argument('fullname')
user_req_args.add_argument('username', help = "username required")
user_req_args.add_argument('email', required = True, help = "email required")
user_req_args.add_argument('password', help = "password required")
user_req_args.add_argument('picture', type=werkzeug.datastructures.FileStorage, location='files')
user_req_args.add_argument('about')

user_fields = {
    'fullname' : fields.String,
    'username' : fields.String ,
    'email' : fields.String
}

class UserAPI(Resource):
    @auth_required('token')
    @cache.memoize(5)
    def get(self, email):
        wrkng_dir = os.path.abspath(os.path.dirname(__file__))
        ppath=os.path.join(wrkng_dir, "static/POST/")
        upath=os.path.join(wrkng_dir, "static/PROFILE/")
        u = user_model.query.filter_by(email = email).first()
        p = Profile.query.filter_by(user_id = u.user_name).first()
        fr = Follow.query.filter_by(profile_id = p.profile_id).count()
        fl = Follow.query.filter_by(user_id = u.user_name).count()
        post = Post.query.filter_by(user_id = u.user_name).all()
        posts=[]
        for p_ in post:
            if(p_.image):
                p_encoded = base64.b64encode(open(ppath+str(p_.image), "rb").read())
                p_new_encode = str(p_encoded)[2:-3]
                p_eng_g=str(p_new_encode)
        
                posts_dict={'post_id': p_.post_id, 'image':p_eng_g, 'heading': p_.heading, 'description': p_.description, 'timestamp': p_.timestamp}
                posts.append(posts_dict)
            else:
                posts_dict={'post_id': p_.post_id, 'image':None, 'heading': p_.heading, 'description': p_.description, 'timestamp': p_.timestamp}
                posts.append(posts_dict)
     
        user_id = u.user_name 
        followers = fr
        following = fl
        post_count = p.total_post
        about = p.about
        prof_encoded = base64.b64encode(open(upath+str(p.profile_pic), "rb").read())
        prof_new_encode = str(prof_encoded)[2:-3]
        prof_eng_g=str(prof_new_encode)
        dp = prof_eng_g
        fullname = u.full_name

        return jsonify(user_id, followers, following, post_count, about, dp, fullname, posts)
    
    @auth_required('token')
    def put(self, email):
            u = user_model.query.filter_by(email = email).first()
            # args = user_req_args.parse_args()

            # eid=email
            eid = request.form.get('email')
            fullname = request.form.get('fullname')
            about = request.form.get('about')
            p_img = request.files.get('p_image')

            p = Profile.query.filter_by(user_id = u.user_name).first()
            fr = Follow.query.filter_by(profile_id = p.profile_id).count()
            fl = Follow.query.filter_by(user_id = u.user_name).count()
            wrkng_dir = os.path.abspath(os.path.dirname(__file__))
            path=os.path.join(wrkng_dir, "static/PROFILE") 
            dpname = ""
            if p_img:
                dpname = "{us}.jpeg".format(us = eid)
                p_img.save(os.path.join(path, dpname))
                user_model.query.filter_by(email = email).update(dict(full_name = fullname))
                Profile.query.filter_by(user_id = u.user_name).update(dict(about = about, profile_pic = dpname))
                db.session.commit()
            # user_model.query.filter_by(email = email).update(dict(full_name = fullname))
            # Profile.query.filter_by(user_id = u.user_name).update(dict(about = about))
            # db.session.commit()
            return jsonify("Profile Updated")
        # except:
        #     return jsonify({"error": "Invalid user or db error"})

    @marshal_with(user_fields)
    def post(self):
        args = user_req_args.parse_args()
        
        fullname = args.get("fullname")
        username = args.get("username")
        email = args.get("email")
        password = args.get("password")
        check=user_model.query.filter_by(email=email).first()
        un_check = user_model.query.filter_by(user_name = username).first()

        if check:
            return ({'error':'email you entered already belongs to an account. Try another email.'}), 400
        elif un_check:
            return ({'error':'username you entered already belongs to an account. Try another username.'}), 500
        else:    
            user_datastore.create_user(email=email, 
                                    full_name = fullname,
                                    user_name=username,
                                    password=hash_password(password))
            p = Profile(user_id = username, profile_pic = "no-profile.jpg", total_post = 0)
            db.session.add(p)
            db.session.commit()
            u_data = user_model.query.filter_by(email=email).first()
            p_data = Profile.query.filter_by(user_id=u_data.user_name).first()
            return jsonify("u_data, p_data"), 200

    @auth_required('token')
    def delete(self, email):
        u=user_model.query.filter_by(email=email).first()
        user_model.query.filter_by(email = email).delete()
        Profile.query.filter_by(user_id = u.user_name).delete()
        Follow.query.filter_by(user_id = u.user_name).delete()
        Post.query.filter_by(user_id = u.user_name).delete()
        db.session.commit()
        return jsonify("User Deleted")


blog_req_args=reqparse.RequestParser()
blog_req_args.add_argument('email', required=True, help="email required")
blog_req_args.add_argument('heading', help="heading required")
blog_req_args.add_argument('description', help="description required")
blog_req_args.add_argument('b_image', type=werkzeug.datastructures.FileStorage, location='files')
blog_req_args.add_argument('timestamp', help="timestamp required")

class BlogAPI(Resource):
    @auth_required('token')
    def get(self, email):
        try:
            u = user_model.query.filter_by(email = email).first()
            # post = Post.query.filter_by(user_id = u.user_name).all()
            post = u.post
            cnt=0
            posts={}
            for p_ in post:
                cnt+=1
                posts_dict={'post_id': p_.post_id, 'image':p_.image, 'heading': p_.heading, 'description': p_.description, 'timestamp': p_.timestamp}
                posts[cnt]=posts_dict
            return jsonify(posts)
        except:
            return jsonify({"error": "Wrong details or database issue"})

    @auth_required('token')    
    def post(self, email):
        u = user_model.query.filter_by(email = email).first()
        p = Profile.query.filter_by(user_id = u.user_name).first()
        wrkng_dir = os.path.abspath(os.path.dirname(__file__))
        path=os.path.join(wrkng_dir, "static/POST/")
        # agrs=blog_req_args.parse_args()
        eid = request.form.get('email')
        heading = request.form.get('heading')
        description = request.form.get('description')
        b_img = request.files.get('b_image')
        print("b_img")
        dt = datetime.datetime.now()
        n=Post.query.count()
        if b_img:
            
            filename=secure_filename(b_img.filename)
            print(filename)
            imgname = filename

            b_img.save(os.path.join(path, imgname))
            tp = p.total_post + 1
            Profile.query.filter_by(user_id = u.user_name).update(dict(total_post = tp))
            db.session.commit()
            post = Post(user_id = u.user_name, image = imgname, heading = heading, description = description,
                timestamp = dt)
            db.session.add(post)
            db.session.commit()
        else:
            print("Entered")
            tp = p.total_post + 1
            Profile.query.filter_by(user_id = u.user_name).update(dict(total_post = tp))
            db.session.commit()
            post = Post(user_id = u.user_name, heading = heading, description = description,
                timestamp = dt)
            db.session.add(post)
            db.session.commit()
            print("Done")
        return jsonify("Blog Created")

    @auth_required('token')
    def put(self, email, post_id):
        try:
            u = user_model.query.filter_by(email = email).first()
            p = Profile.query.filter_by(user_id = u.user_name).first()
            wrkng_dir = os.path.abspath(os.path.dirname(__file__))
            path=os.path.join(wrkng_dir, "static/POST/")
            eid = email
            heading = request.form.get('heading')
            description = request.form.get('description')
            b_img = request.files.get('b_image')
            filename=secure_filename(b_img.filename)
            if b_img:
                imgname = filename
                b_img.save(os.path.join(path, imgname))
                post = Post.query.filter_by(post_id=post_id).update(dict(image = imgname, heading = heading, description = description))
                db.session.commit()
            else:
                post = Post.query.filter_by(post_id=post_id).update(dict(heading = heading, description = description))
                db.session.commit()
            return jsonify("Blog Updated")
        except:
            return jsonify("Post Error")

    @auth_required('token')    
    def delete(self, email, post_id):
        try:
            u=user_model.query.filter_by(email=email).first()
            de = Profile.query.filter_by(user_id = u.user_name).first()
            tpo = de.total_post - 1
            Profile.query.filter_by(user_id = u.user_name).update(dict(total_post = tpo))
            Post.query.filter_by(post_id=post_id).delete()
            db.session.commit()
            return jsonify("Blog Deleted Successfully")
        except:
            return jsonify("Server Error")


search_req_args=reqparse.RequestParser()
search_req_args.add_argument('email', required=True, help="email required")

class SearchAPI(Resource):
    @auth_required('token')
    def get(self, email, sea):
        u = user_model.query.filter_by(email = email).first()
        results={}
        if sea:
            element = "%" + sea + "%"
            result = Profile.query.filter(Profile.user_id.like(element)).all()
            for i in result:
                if(i.user_id!=u.user_name):
                    results[i.profile_id]={'user_id':i.user_id, 'profile_id':i.profile_id, 'about':i.about}
        return jsonify(results)
    


class FollowerAPI(Resource):
    @auth_required('token')
    def get(self, email):
        u = user_model.query.filter_by(email = email).first()
        p = Profile.query.filter_by(user_id = u.user_name).first()
        fr = Follow.query.filter_by(profile_id = p.profile_id).count()
        fl = Follow.query.filter_by(user_id = u.user_name).count()
        following = Follow.query.filter_by(user_id=u.user_name).all()
        following_pids=[]
        followings={}
        following_stats={}
        for i in following:
            x = Profile.query.filter_by(profile_id=i.profile_id).first()
            frs=Follow.query.filter_by(profile_id = x.profile_id).count()
            fings=Follow.query.filter_by(user_id = x.profile_id).count()
            following_pids.append(x.user_id)
            following_stats[i.profile_id]={'user': x.user_id, 'profile_id': i.profile_id, 'total_posts':x.total_post, 'followers':frs, 'following':fings}

        userfeed_posts={}
        for i in following_pids:
            pst = Post.query.filter_by(user_id=i).all()
            f_psts=[]
            for j in pst:
                wrkng_dir = os.path.abspath(os.path.dirname(__file__))
                path=os.path.join(wrkng_dir, "static/POST/")
                if(j.image):
                    post_ = base64.b64encode(open(path+j.image, "rb").read())
                    new_post_ = str(post_)[2:-3]
                    npe=str(new_post_)
                    u_p=Profile.query.filter_by(user_id = j.user_id).first()
                    post_dict={'post_id': j.post_id, 'profile_id':u_p.profile_id, 'user': j.user_id, 'image':npe, 'heading':j.heading, 'description':j.description, 'timestamp':j.timestamp}
                    fing_post_dict={'post_id': j.post_id, 'user': j.user_id, 'image':npe, 'heading':j.heading, 'description':j.description, 'timestamp':j.timestamp}
                    userfeed_posts[j.post_id] = post_dict
                    f_psts.append(fing_post_dict)
                else:
                    u_p=Profile.query.filter_by(user_id = j.user_id).first()
                    post_dict={'post_id': j.post_id, 'profile_id':u_p.profile_id, 'user': j.user_id, 'image':j.image, 'heading':j.heading, 'description':j.description, 'timestamp':j.timestamp}
                    fing_post_dict={'post_id': j.post_id, 'user': j.user_id, 'image':j.image, 'heading':j.heading, 'description':j.description, 'timestamp':j.timestamp}
                    userfeed_posts[j.post_id] = post_dict
                    f_psts.append(fing_post_dict)
            followings[i]=f_psts

        follower = Follow.query.filter_by(profile_id=p.profile_id).all()
        followers_pids=[]
        followers={}
        follower_stats={}
        for i in follower:
            x = Profile.query.filter_by(user_id=i.user_id).first()
            frs=Follow.query.filter_by(profile_id = x.profile_id).count()
            fings=Follow.query.filter_by(user_id = x.user_id).count()
            followers_pids.append(x.user_id)
            follower_stats[x.profile_id]={'profile_id': x.profile_id, 'user': i.user_id, 'total_posts':x.total_post, 'followers':frs, 'following':fings}

        for i in followers_pids:
            pst = Post.query.filter_by(user_id=i).all()
            f_psts=[]
            for j in pst:
                frs_post_dict={'post_id': j.post_id, 'user': j.user_id, 'image':j.image, 'heading':j.heading, 'description':j.description, 'timestamp':j.timestamp}
                f_psts.append(frs_post_dict)
            followers[i]=f_psts
        wrkng_dir = os.path.abspath(os.path.dirname(__file__))
        path=os.path.join(wrkng_dir, "static/PROFILE/")
        if(u.email+".jpeg" == p.profile_pic):
            encoded = base64.b64encode(open(path+u.email+".jpeg", "rb").read())
            new_encode = str(encoded)[2:-3]
            prof=str(new_encode)
        else:
            encoded = base64.b64encode(open(path+"no-profile.jpg", "rb").read())
            new_encode = str(encoded)[2:-3]
            prof=str(new_encode)        
        u_d={}
        u_d['fullname']=u.full_name
        u_d['dp']=prof
        u_d['username']=u.user_name
        u_d['total_posts']=p.total_post
        u_d['followers']=fr
        u_d['following']=fl
        u_d['profile']=prof
        return jsonify(u_d, followings, following_stats, followers, follower_stats, userfeed_posts)
    
    @auth_required('token')
    def post(self, email, profile_id):
        # s="ham follow krenge kisiko yani following krne ya badhane ke liye uska profile bhi aayega"
        u=user_model.query.filter_by(email=email).first()
        p1 = Profile.query.filter_by(user_id = u.user_name).first()
        p2 = Profile.query.filter_by(profile_id = profile_id).first()
        
        chk = Follow.query.filter_by(user_id=u.user_name).filter_by(profile_id=p2.profile_id).first()
        if(chk):
            pass
        else: 
            n_e = Follow(user_id=u.user_name, profile_id=p2.profile_id)
            db.session.add(n_e) 
            db.session.commit()
        return jsonify("Followed")
    
    @auth_required('token')
    def put(self, email, profile_id):
        try:
            # s="unfollow krne ke liye"
            u=user_model.query.filter_by(email=email).first()
            p1 = Profile.query.filter_by(user_id = u.user_name).first()
            p2 = Profile.query.filter_by(profile_id = profile_id).first()

            chk = Follow.query.filter_by(user_id = p1.user_id).filter_by(profile_id = p2.profile_id).first()
            if(chk):
                Follow.query.filter_by(user_id = p1.user_id).filter_by(profile_id = p2.profile_id).delete()
                db.session.commit()
            else: 
                pass
            return jsonify("unfollowed")
        except:
            return jsonify("cant unfollow")


comment_req_args=reqparse.RequestParser()
comment_req_args.add_argument('email')
comment_req_args.add_argument('post_id')
comment_req_args.add_argument('comment')



class EngagementAPI(Resource):
    @auth_required('token')
    @cache.memoize(50)
    def get(self, email):
        import matplotlib.pyplot as plt
        wrkng_dir = os.path.abspath(os.path.dirname(__file__))
        path=os.path.join(wrkng_dir, "static/IMG/")
        u = user_model.query.filter_by(email = email).first()
        p = Profile.query.filter_by(user_id = u.user_name).first()
        fr = Follow.query.filter_by(profile_id = p.profile_id).count()
        fl = Follow.query.filter_by(user_id = u.user_name).count()
        up = Post.query.filter_by(user_id=u.user_name).all()
        plt.clf()
        plt.plot([x.heading for x in up], [x.timestamp for x in up], c='r', marker='o')
        plt.ylabel("Time Stamp")
        plt.xlabel("Heading")
        plt.yticks(rotation = 45)
        plt.savefig(path+u.user_name+".png")
        encoded = base64.b64encode(open(path+u.user_name+".png", "rb").read())
        new_encode = str(encoded)[2:-3]
        eng_g=str(new_encode)
        u_d={}
        u_d['username']=u.user_name
        u_d['total_posts']=p.total_post
        u_d['followers']=fr
        u_d['following']=fl
        return jsonify(u_d, eng_g)
    
class ExportBlogAPI(Resource):
    @auth_required('token')
    def get(self, email):
        try:

            user = user_model.query.filter_by(email = email).first()
            username = user.user_name
            
            posts  = user.post
            if(posts):
                post_ids = []
                for i in posts:
                    post_ids.append(i.post_id)
                details = []    
                for j in post_ids:    
                    detail = Post.query.filter_by(post_id=j).first()
                    details.append(detail)
                cnt = 0  
                l = []
                for k in details:
                    cnt+=1
                    blog_dict = {"SNo":cnt ,"Heading":k.heading,"Description":k.description, "Date_Created": str(k.timestamp)}
                    l.append(blog_dict)
                Blog_exp = tasks.export_blog.delay(l, username, email)
                return jsonify("Blogs Exported")
            else:
                raise Exception("No blogs to export")
        except:
            return jsonify("Couldn't export")
    
class OtherUserAPI(Resource):
    @auth_required('token')
    def get(self, email, profile_id):
        try:
            wrkng_dir = os.path.abspath(os.path.dirname(__file__))
            path=os.path.join(wrkng_dir, "static/PROFILE/")
            path_=os.path.join(wrkng_dir, "static/POST/")
            u=user_model.query.filter_by(email=email).first()
            p=Profile.query.filter_by(profile_id=profile_id).first()
            posts = Post.query.filter_by(user_id = p.user_id).all()
            p_u=user_model.query.filter_by(user_name=p.user_id).first()
            oupd={}
            psts = {}
            for i in posts:
                post_encoded = base64.b64encode(open(path_+i.image, "rb").read())
                post_new_encode = str(post_encoded)[2:-3]
                post_eng_g=str(post_new_encode)

                psts[i.post_id] = {'post_id':i.post_id, 'image':post_eng_g, 'heading':i.heading, 'description':i.description, 'timestamp':i.timestamp}
            oupd['fullname'] = p_u.full_name
            oupd['user_name'] = p_u.user_name
            oupd['email'] = p_u.email
            oupd['profile_id'] = p.profile_id
            oupd['about'] = p.about
            oupd['total_post'] = p.total_post
            oupd['follower'] = Follow.query.filter_by(user_id = p.user_id).count()
            oupd['following'] = Follow.query.filter_by(profile_id = profile_id).count()
            prof_encoded = base64.b64encode(open(path+p.profile_pic, "rb").read())
            prof_new_encode = str(prof_encoded)[2:-3]
            prof_eng_g=str(prof_new_encode)
        
            oupd['profile_pic'] = prof_eng_g
            oupd['post'] = psts
            return jsonify(oupd)
        except:
            return jsonify({"error":"Internal or server error"})