<template>
    <div class="home">
        <SideBar />

        <!-- Blog-section -->
        <section id="blog">
            <!-- heading -->
            <div class="blog-heading">
                <h3>Blog-Look</h3>
                <span>Latest Blogs</span>
            </div>

            <!-- blog container -->
            <div class="blog-container">
                <p align="middle" class="alert alert-danger" v-if="error">{{ error }}</p>
                <p align="middle" class="alert alert-success" v-if="good">{{ good }}</p>
                <div v-for="value in userfeed_post" :key="value.post_id"> 

                    <!-- box-1 -->
                    <div class="blog-box">
                        <!-- blog image --> 
                        <div class="blog-image" v-if="value.image">
                            <img :src="`data:image/png;base64,${value.image}`" alt="image not found" style="height: 250px;" />
                        </div>
                        <!-- text -->
                        <div class="blog-text">
                            <span style="font-size: 1rem;margin-bottom: 30px;">{{ value.timestamp }}</span>
                            <span style="margin-bottom: 20px;color: blue;">
                                <i class="ri-user-line">
                                    <router-link to="/otherprofile" v-on:click="store(value.profile_id)" style="color: blue">{{ value.user }}</router-link>
                                </i>
                                </span>
                            <a href="#" class="blog-title">
                                <span v-html = "value.heading"></span>
                            </a>
                            <p class="blog-section">
                                <span v-html = "value.description"></span>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
import SideBar from './SideBar.vue';
    export default {
    name: "HomePage",
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
        following: {},
        following_stat: {},
        follower: {},
        follower_stat: {},
        userfeed_post: {}
        };
    },
    async created() {
        this.auth_token = sessionStorage.getItem("auth-token")
        this.email = sessionStorage.getItem("email")
        console.log(this.email)
        if(!this.auth_token){
        alert("Login to view your Dashboard")
        this.$router.push("/")
        }
        return fetch(`http://127.0.0.1:5000/api/followaction/${this.email}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authentication-Token": `${this.auth_token}`
        }
        }).then((response) => response.json())
        .then((data) => {
        this.u=data[0]
        localStorage.setItem('username', this.u.username)
        localStorage.setItem('fullname', this.u.fullname)
        localStorage.setItem('total_posts', this.u.total_posts)
        localStorage.setItem('followers', this.u.followers)
        localStorage.setItem('following', this.u.following)
        localStorage.setItem('profile', this.u.profile)
        this.following = data[1]
        this.following_stat = data[2]
        this.follower = data[3]
        this.follower_stat = data[4]
        this.userfeed_post = data[5]
        console.log(data)
        }).catch((error) => console.log("1st", error))
    },
    methods: {
        async store(profile_id){
            localStorage.setItem('profile_id', profile_id)
        }
    }
    };
</script>

<style scoped>
.main-home {
    padding: 0px;
    overflow: hidden;
    top: 5px;
}

a{
    text-decoration: none;
}

ul{
    list-style: none;
}

#blog{
    /* display: flex; */
    justify-content: center;
    align-items: center;
    /* flex-direction: row; */
    flex-wrap: wrap;
    padding: 40px;
    margin-left: 250px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
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
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin: 20px 0px;
    flex-wrap: wrap;
}
.blog-box{
    width:350px;
    background-color: white;
    border: 3px solid black;
    box-shadow: gray 5px 5px 10px;
    margin: 20px;
    left:0px; 
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
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
}

.blog-text{
    padding: 30px;
    display: flex;
    flex-direction: column;
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

</style>
