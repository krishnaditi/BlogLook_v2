<template>
    <div class="home">
        <SideBar />

        <div class="p_page">

            <p align="middle" class="alert alert-danger" v-if="error">{{ error }}</p>
            <p align="middle" class="alert alert-success" v-if="good">{{ good }}</p>

            <!-- profile image -->
            <div class="p_image">
                <img :src="`data:image/png;base64,${other_details.profile_pic}`" alt="image not found" />
            </div>

            <div class="p_name">
                <h1>{{ other_details.fullname }}</h1>
                <span>{{ other_details.user_name }}</span>
            </div>

            <div class="p_data">

                <!-- total posts -->
                <div class="p_details">
                    <h2>Total Posts</h2>
                    <p>{{ other_details.total_post }}</p>
                </div>

                <!-- followers -->
                <div class="p_details">
                    <h2>Followers</h2>
                    <p>{{ other_details.follower }}</p>
                </div>

                <!-- following -->
                <div class="p_details">
                    <h2>Following</h2>
                    <p>{{ other_details.following }}</p>
                </div>

            </div>   
            
            <!-- about -->
            <div class="p_about">
                <h2>About</h2>
                <p>
                    {{ other_details.about }}
                </p>
            </div>
        </div>

        <!-- blog container -->
        <div class="blog-container">
        <!-- box-1 -->
                <div v-for="v in other_details.post" :key="v.post_id" class="blog-box">

                    <!-- blog image -->

                    <div class="blog-image" v-if="v.image">
                        <img :src="`data:image/png;base64,${v.image}`" alt="image not found" />
                    </div>

                    <!-- text -->
                    <div class="blog-text">
                        <span style="font-size: 1rem;margin-bottom: 30px;">{{ v.timestamp }}</span>
                        <span style="margin-bottom: 20px;color: blue;">
                            <i class="ri-user-line">
                                <router-link to="/otherprofile" v-on:click="store(v.profile_id)" style="color: blue">{{ other_details.user_name }}</router-link>
                            </i></span>
                        <h3 class="blog-title">{{ v.heading }}</h3>
                        <p>{{ v.description }}</p>
                    </div>
                </div>
        </div>    
    </div>
</template>
<script>
import SideBar from './SideBar.vue';
    export default {
    name: "OtherProfile",
    components: {
        SideBar
    },
    data() {
        return {
        u: {},
        email: null,
        auth_token: null,
        error: "",
        good: "",
        other_details: null
        };
    },
    async created() {
        this.auth_token = sessionStorage.getItem("auth-token")
        this.email = sessionStorage.getItem("email")
        this.profile_id = localStorage.getItem("profile_id")
        console.log(this.email)
        if(!this.auth_token){
            alert("Login to view your Dashboard")
            this.$router.push("/")
        }
        return fetch(`http://127.0.0.1:5000/api/userprofile/${this.email}`+"/"+`${this.profile_id}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authentication-Token": `${this.auth_token}`
        }
        }).then((response) => response.json())
        .then((data) => {
        this.other_details=data
        console.log(data)
        }).catch((error) => console.log("1st", error))
    },
    methods: {
        store(profile_id){
            localStorage.setItem("profile_id", profile_id)
        }
    }
    }
</script>

<style scoped>

.p_page {
    background: url(../assets/p_background.jpg) no-repeat center/cover;
    border-radius: 0px;
    color: #fdfffb;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-top: 0rem;
    /* border: 1px solid red; */
    min-height: 250px;
    position:relative;
    width : 1050px;
    left: 300px;
}

.p_image {
    display: flex;
    position: absolute;
    align-items: center;
    justify-content: center;
    width: 150px;
    height: 150px;
    border-radius: 50%;
    border: 2px solid red;
    left: 25px;
    bottom: 70px;
}

.p_image img {
    width: 140px;
    height: 140px;
    object-fit: cover;
    border-radius: 50%;
    object-position: center;
}

.p_name {
    display: flex;
    position: absolute;
    margin: 1rem 0 0.4rem;
    left: 200px;
    top: 40px;
    /* border: 1px solid red; */
}

.p_name h1 {
    position: absolute;
    font-size: 2rem;
    width: 100px;
    /* border: 1px solid green; */
}

.p_name span{
    font-size: 1.5rem;
    position: absolute;
    top: 50px;
    min-width: 200px;
    font-weight: bold;
    /* border: 1px solid red; */
    text-align: left;
}

.pbtn button{
    display: block;
    position: absolute;
    text-decoration: none;
    border: 1px solid gray;
    padding: 2px;
    width: 100px;
    color: black;
    font-weight: bold;
    text-align: center;
    left: 5%;
    bottom: 25px;
    font-size: 1.0rem;
    cursor: pointer;
}

.pbtn button:hover{
    color: wheat;
    background: #05f7ff; 
}

.pbtn h3 {
        font-size: 1rem;
        font-weight: bold;
        color: black;
}

.ebtn button{
    display: block;
    position: absolute;
    text-decoration: none;
    /* border: 1px solid gray; */
    padding: 2px;
    width: 100px;
    color: black;
    font-weight: bold;
    text-align: center;
    right: 10px;
    bottom: 20px;
    z-index: 99;
    font-size: 1.0rem;
    cursor: pointer;
}

.ebtn button:hover{
    color: wheat;
    background: #05f7ff; 
}

.ebtn h3 {
        font-size: 1rem;
        font-weight: bold;
        color: black;
}

.exbtn button{
    /* border: 1px solid red; */
    position: absolute;
    bottom:20px;
    right: 210px;
    width: 100px;
    display: block;
    text-decoration: none;
    padding: 2px;
    color: black;
    font-weight: bold;
    text-align: center;
    z-index: 99;
    font-size: 1.0rem;
    cursor: pointer;
}

.exbtn button:hover{
    color: black;
    background: #05f7ff; 
}

.p_data {
    /* border: 1px solid red; */
    padding: 10px;
    display: flex;
    justify-content: space-between;
    margin-bottom: 80px;
    min-width:600px;
    right: 40px;
    position: absolute;
}

.p_details{
    padding: 8px;
    font-size: 1.5rem;
    min-width: 80px;
    min-height: 80px;
    /* border: 1px solid blue; */
    text-align: center;
    margin: 17px;
}


.p_details h2 {
    font-weight: 500;
    right: 10px;

}

.p_about{
    /* border: 1px solid green; */
    bottom: 5px;
    position: absolute;
    width: 810px;
    float: right;
    left: 200px;
    text-align: left;
}

#del:hover{
    color: rgb(221, 0, 0);
    cursor: pointer;
}

#del{
    /* border: 1px solid red; */
    margin-right: 40px;
    margin-left: 190px;
    width: 20px;
    margin-top: 0px;
    margin-bottom: 100px;
    position:absolute;
    color: blue;
    float: right;
}

#blog{
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    padding: 40px;
    /* border: 3px solid red; */
}

.blog-heading{
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}

.blog-heading span{
    color: #f33c3c;
    font-size: 1.7rem;
    text-shadow: brown 2px 2px 5px;
    text-decoration: underline;
}

.blog-heading h3{
    font-size: 2.5rem;
    color: black;
    padding: 10px;
    font-weight: bold;
    font-weight: 600;
    text-shadow: gray 2px 2px 5px;
}

.blog-container{
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 30px 0px;
    flex-wrap: wrap;
}

.blog-box{
    width:350px;
    background-color: white;
    border: 3px solid black;
    box-shadow: gray 5px 5px 10px;
    margin: 80px;
    left:150px; 
    top: 30px; 
    position: relative;
}

.blog-image{
    width: 100%;
    height: auto;
}

.blog-image i{
    justify-content: left;
    text-align: left;
    /* border: 1px solid red; */
    margin-left: 50px;
    margin: 2px;
    font-weight: bold;
    font-size: 1rem;
}

#edit:hover{
    color: palevioletred;
    cursor: pointer;
}

#comment:hover{
    color: green;
    cursor: pointer;
}

.blog-image img{
    width: 250px;
    height: 300px;
    object-fit: cover;
    object-position: center;
}

.blog-text{
    padding: 30px;
    display: flex;
    flex-direction: column;
    /* border: 1px solid green; */
}

.blog-text span{
    /* border: 1px solid red; */
    font-size: 1.5rem;
    text-align: center;
    justify-content: center;
    margin: 0px;
    margin-top: 0%;
}

.blog-text .blog-title{
    font-size: 1.3rem;
    font-weight: 500;
    color: #2b2b2b;
}

.blog-text p{
    color: gray;
    font-size: 0.9rem;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    margin: 20px 0px;
}

.blog-text a{
    color: black;
}
#bdel{
    float:right;
    font-size:1.8rem;
    /* border: 1px solid red; */
    width:40px;
    color: black;
}
#bdel:hover{
    background-color: red;
    color: wheat;
    cursor: pointer;
}
#bedit{
    float:left;
    font-size: 1.8rem;
    /* border: 1px solid green; */
    width:40px;
    color: black;
}
#bedit:hover{
    cursor:pointer;
    background-color: green;
    color: wheat;
}
#pc:hover{
    color:white;
}
#rb:hover{
    color: white;
}

</style>