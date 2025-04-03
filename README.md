# <img src="https://img.icons8.com/ios-filled/50/000000/blog.png" width="25"/> BlogLook Application
 
_A Social Platform for Blog Management using Flask, SQLAlchemy, VueJS & Bootstrap_  

![Python](https://img.shields.io/badge/Python-3.8-blue)  ![Flask](https://img.shields.io/badge/Flask-2.0-blue)  ![Vue.js](https://img.shields.io/badge/Vue.js-3.0-42b883?logo=vue.js)  ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4-green)  ![Bootstrap](https://img.shields.io/badge/Bootstrap-5.0-purple?logo=bootstrap)  ![Celery](https://img.shields.io/badge/Celery-5.2-green?logo=celery)  ![Redis](https://img.shields.io/badge/Redis-7.0-red?logo=redis)  ![MailHog](https://img.shields.io/badge/MailHog-Email%20Testing-orange)

## 📌 About The Project  
The BlogLook Application is a web platform that allows users to socially connect with other users and then can manage their blogs. 

### 🔹 Key Features  
✔️ Social Application  
✔️ Blog Management workflow  
✔️ Following & Follower System  
✔️ Caching done by Redis server 
✔️ Monthly and Daily Reminders System for users


## 🛠️ Tech Stack  
- **Backend:** Flask, SQLAlchemy  
- **Frontend:** VueJS, Bootstrap  
- **Database:** SQLite  
- **Caching:** Redis
- **Jobs:** Celery  

## ⚙️ Installation  
1. Clone the repository  
   ```sh
   git clone https://github.com/your-username/household-services.git
   cd household-services

2. python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. pip install -r requirements.txt

4. flask run

## 📂 Folder Structure  

/BlogLook_v2 
│-- backend 
│   --├── application      # Backend folder 
│         --├── static    # images and csv files
│         --├── templates    # HTML pages for triggered jobs
│            ├── api.py    # flask apis
│            ├── cache.py    # cache initilization
│            ├── clry.py    # celery initilization
│            ├── emailgen.py    # SMTP initilization
│            ├── models.py    # database tables
│            ├── tasks.py    # jobs triggered
│      ├── 21f1004270-Project Documentation.pdf      # Project Report 
│      ├── app.py     # configuration and API endpoints
│      ├── requirements.txt     # libraries used

│-- frontend 
│   --├── src  
│         --├── assets         # Images
│         --├── components         # vue components        
│                 ├── Add_Blogs.vue         
│                 ├── DeleteBlog.vue          
│                 ├── DeleteUser.vue         
│                 ├── EngageMent.vue         
│                 ├── FollowersPg.vue         
│                 ├── FollowingPg.vue         
│                 ├── HomePage.vue         
│                 ├── LoginPage.vue          
│                 ├── MyProfile.vue          
│                 ├── OtherProfile.vue         
│                 ├── 
│                 ├── ...
│         --├── router
│         --├── store
│         --├── views
│            ├── App.vue
│            ├── main.js
   
│-- README.md
│-- openapi.yaml


## 👤 Author  
**Aditi Krishana**  
🔗 [GitHub](https://github.com/krishnaditi) | [LinkedIn](https://linkedin.com/in/aditi-krishana)  
📧 Email: krishanaaditi@gmail.com  

## 🎉 Acknowledgments  
Thanks to [Bootstrap](https://getbootstrap.com/) & [Flask](https://flask.palletsprojects.com/) for making this project possible.

