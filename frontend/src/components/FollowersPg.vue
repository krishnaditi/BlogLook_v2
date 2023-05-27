<template>
    <div class="home">
        <SideBar />

        <div class="followers" style="display: flex;align-items: center;
        justify-content: center;">

            <p align="middle" class="alert alert-danger" v-if="error">{{ error }}</p>
            <p align="middle" class="alert alert-success" v-if="good">{{ good }}</p>

            <div class="follow" style="text-decoration: underline;">
                Your Followers
            </div>

                <div class="fl" style="width: 600px;margin: 20px 0px;font-size: 1.2rem;
                                    font-weight: bold;text-align: left;
                                    height: 55px;position: relative;"
                                    v-for="value in follower_stat" :key="value.profile_id">
                
                <router-link to="/otherprofile">
                    <h1 v-on:click="store(value.profile_id)">{{ value.user }}
                    </h1>
                </router-link>

                <router-link :to="`/follow/${value.profile_id}`">
                    <button  id = "fl" style="position: absolute; right:110px; top:10px;
                                        font-size: 1.4rem; font-weight: bold; 
                                        padding: 3px;" 
                                        @click="follow(value.profile_id); storeData(value.user_id); store(value.profile_id)">
                    Follow
                    </button>
                </router-link>

                <router-link :to="`/unfollow/${value.profile_id}`">
                    <button  id = "uf" style="position: absolute;right: 0px;top:10px;
                                        font-size: 1.4rem; font-weight: bold;
                                        padding: 3px;" 
                                        @click="unfollow(value.profile_id); storeData(value.user_id); store(value.profile_id)">
                    Unfollow
                    </button>
                </router-link>

                </div>
        </div>
    </div>
</template>
<script>
import SideBar from './SideBar.vue';
    export default {
    name: "FollowersPg",
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
        },
        async follow(profile_id){
        this.profile_id=profile_id;
        localStorage.setItem("profile_id",profile_id);
        try {
        fetch("http://127.0.0.1:5000/api/followaction/"+`${this.email}`+"/"+`${this.profile_id}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json;charset=utf-8",
                "Authentication-Token": `${this.auth_token}`,
            },                
            body: JSON.stringify({
                email: this.email,      
                profile_id : this.profile_id,
            }),
        })
        .then((resp) =>  resp.json())
        .then((data) => {
            const response = data;
            if (response.message) {
                this.error = response.message;
                console.log(response.message);
            } else {
                console.log("Followed");
                this.$router.go(-1);
                this.good='Followed'
            }
        })
        .catch((error) => {
            console.log("1st",error);
        });
        } catch (error) {
            console.log("2nd",error);
        }
    },
    async unfollow(profile_id){
        this.profile_id=profile_id;
        localStorage.setItem("profile_id",profile_id);
        try {
        fetch("http://127.0.0.1:5000/api/followaction/"+`${this.email}`+"/"+`${this.profile_id}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json;charset=utf-8",
                "Authentication-Token": `${this.auth_token}`,
            },                
            body: JSON.stringify({
                email: this.email,      
                profile_id : this.profile_id,
            }),
        })
        .then((resp) =>  resp.json())
        .then((data) => {
            const response = data;
            if (response.message) {
                this.error = response.message;
                console.log(response.message);
            } else {
                console.log("Unfollowed");
                this.$router.go(-1)
                this.good='Unfollowed'
            }
        })
        .catch((error) => {
            console.log("1st",error);
        });
        } catch (error) {
            console.log("2nd",error);
        }
    },
    }
    };
</script>


<style scoped>

.followers{
    padding: 0px;
    margin: 0px;
    /* border: 1px solid red; */
    background: url(../assets/ab.jpg) no-repeat center/cover;
    background-color: transparent;
    height: 99vh;
    width: 1066px;
    float: right;
    flex-direction: column;
}

 .follow{
    /* border: 1px solid red; */
    position: absolute;
    font-size: 3rem;
    padding: 3px;
    font-weight: bold;
    margin-top: 0px;
    margin-left: 400px;
    margin-right: 400px;
    margin-bottom: 450px;
    width: 300px;
    color: rgb(39, 33, 33);
    text-shadow: 3px 3px 6px rgb(107, 42, 42);
    text-decoration: underline;
}

#fl{
    position: absolute;
    border: 3px solid green;
    right: 200px;
    font-size: 1.8rem;
}

#fl:hover{
    background: green;
    color: white;
    cursor: pointer;
    border: 2px solid black;
}

#uf{
    position: absolute;
    right: 0px;
    font-size: 1.8rem;
    border: 3px solid red;
}

#uf:hover{
    background: red;
    color: white;
    cursor: pointer;
    border: 2px solid black;
}


</style>