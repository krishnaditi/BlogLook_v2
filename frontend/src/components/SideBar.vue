<template>
    <!-- sidebar -->
    <div class="sidebar">
        <a href="#" class="logo">
            <img src="../assets/logo.jpg" alt="">
        </a>
        <!-- profile image -->
        <div class="profile">
            <div class="profile-image">
                <img :src="`data:image/png;base64,${this.profile}`" alt="image not found" />
            </div>

            <div class="profile-name">
                <h1>{{ this.full }}</h1>
            </div>
            <span>{{ this.user }}</span> 
        </div>
        <!-- about -->
        <div class="about">

            <!-- box-1 -->
            <div class="box">
                <!-- <h3>{{ post_count }}</h3> -->
                <h3>{{ this.tot }}</h3>
                <span>Posts</span>
            </div>

            <!-- box-2 -->
            <div class="box">
                <router-link to="/followers"><h3>{{ this.follower }}</h3></router-link>
                <span id = "flr">Followers</span>
            </div>

            <!-- box-3 -->
            <div class="box">
                <router-link to="/following"><h3>{{ this.following }}</h3></router-link>
                <span id = "flr">Following</span>
            </div>
        </div>
        <!-- menu -->
        <div class="menu">
            <router-link to="/userfeed">
                <span class="icon">
                    <i class="ri-function-line"></i>
                </span>
                Feed
            </router-link>

            <router-link to="/myprofile">
                <span class="icon">
                    <i class="ri-profile-line"></i>
                </span>
                Profile
            </router-link>

            <router-link to="/Add_Blogs">
                <span class="icon">
                    <i class="ri-add-circle-fill"></i>
                </span>
                Add Blogs
            </router-link>

            <router-link to="/search">
                <span class="icon">
                    <i class="ri-search-line"></i>
                </span>
                Search
            </router-link>

            <router-link to="/delete">
                <span class="icon">
                    <i class="ri-account-circle-line"></i>
                </span>
                Delete Account
            </router-link>


            <router-link to="/" @click="clean">
                <span class="icon">
                    <i class="ri-logout-box-r-line"></i>
                </span>
                Logout
            </router-link>
        </div>
    </div>

</template>

<script>
export default {
  name: 'SideBar',
  data () {
    return{
        auth_token: null,
        email: null,
        user: null,
        full: null,
        tot: null,
        following: null,
        follower: null,
        profile: null,
    }
    },
    async created() {
        this.auth_token = sessionStorage.getItem("auth-token")
        this.email = sessionStorage.getItem("email")
        console.log(this.email)
        if(!this.auth_token){
        alert("Login to view your Dashboard")
        this.$router.push("/")
        }
        await fetch(`http://127.0.0.1:5000/api/followaction/${this.email}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authentication-Token": `${this.auth_token}`
        }
        }).then((response) => response.json())
        .then((data) => {
        this.u=data[0]
        this.user= this.u.username
        this.full= this.u.fullname
        this.tot=this.u.total_posts
        this.follower= this.u.followers
        this.following= this.u.following
        this.profile=this.u.profile
        }).catch((error) => console.log("1st", error))
    },
  methods: {
    async clean() {
        sessionStorage.clear()
        localStorage.clear()
        },
    }
}
</script>

<style>

    /* Google fonts */
    @import url('https://fonts.googleapis.com/css2?family=Yeon+Sung&display=swap');
    * {
        font-family: 'Yeon Sung', 'cursive'; 
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        list-style: none;
        text-decoration: none;
    }


    .sidebar {
        position: fixed;
        width: 300px;
        height: 100vh;
        background: #008489;
        /* z-index: 2; */
        padding: 20px;
    }
    .main-home {
        position: absolute;
        width: calc(100% - 300px);
        top: 0px;
        left: 300px;
        background: white;
        /* border-radius: 1rem 0 0 1rem; */
        /* z-index: 1000; */
    }

    .logo img {
        width: 100px;
        height: 100px;
        border: 5px solid #05f7ff;
        margin-left: 10px; 
    }

    .profile {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin-top: 1.4rem;
        color: black;
        font-size: 1.3rem;
    }

    .profile-image {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100px;
        height: 100px;
        border-radius: 50%;
        border: 3px solid black;
    }

    .profile-image img {
        width: 90px;
        height: 90px;
        object-fit: cover;
        border-radius: 50%;
        object-position: center;
    }

    .profile-image span {
        font-size: 0.938rem;
        font-weight: 400;
    }

    .profile-name {
        display: flex;
        align-items: center;
        margin: 1rem 0 0.4rem;
    }

    .profile-name h1 {
        font-size: 1.6rem;
        color: black;
    }

    .profile-name img {
        margin-left: 4px;
        width: 20px;
        object-fit: contain;
    }

    .profile-name span{
        font-size: 0.5rem;
        position: absolute;
        top: 50px;
        min-width: 200px;
        font-weight: bold;
    }

    .about {
        display: flex;
        justify-content: space-between;
        margin-top: 1rem;
    }

    .box {
        text-align: center;
    }

    .box h3 {
        font-size: 1rem;
        font-weight: 500;
        color: black;
    }

    .box h3:hover{
        color: wheat;
    }

    .box span {
        font-size: 0.938rem;
        font-weight: 400;
        color:black;
    }

    #flr:hover{
        color: wheat;
        cursor: pointer;
    }

    .menu a {
        width: 100%;
        font-size: 1rem;
        color: black;
        display: flex;
        align-items: center;
        line-height: 40px;
    }

    .menu a:hover,
    .menu .active {
        color: wheat;
    }

    .menu .icon {
        margin-right: 1rem;
        font-size: 20px;
    }
</style>