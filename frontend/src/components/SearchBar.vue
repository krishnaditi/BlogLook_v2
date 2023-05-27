<template>
    <div class="all">
        <SideBar />
    
    <div class="search">
        <p align="middle" class="alert alert-success" v-if="good">{{ good }}</p>
        
        <div class="s_bar" align="center">
            <form action="" method="post">
            <input type="text" placeholder="Search" v-model="s">
            <button type="submit" @click.prevent="search()">
            <i class="ri-search-line"></i>
            </button>
            </form>
        </div>

        <div class="res">
            <div v-if="searchresults">
                <div v-for="value in searchresults" :key="value.profile_id" class = "col">
                    <div class="s_name">
                    <router-link to="/otherprofile">
                        <h5 id = "un" align="middle" v-on:click="store(value.profile_id)"><strong>{{ value.user_id }}</strong> </h5>&nbsp;
                    </router-link>
                    <router-link :to="`/follow/${value.profile_id}`" >
                        <button  id = "fl" align="right" @click="follow(value.profile_id); storeData(value.user_id)">Follow</button>
                    </router-link>&nbsp;
                    <router-link :to="`/unfollow/${value.profile_id}`">
                        <button  id = "uf" align="right" @click="unfollow(value.profile_id); storeData(value.user_id)">Unfollow</button>
                    </router-link>
                    </div>
                </div>  
            </div>
        </div>
    </div>
    </div>
</template>

<script>
import router from '@/router';
import SideBar from './SideBar.vue';
    export default {
    name: "SearchBar",
    components: {
        SideBar
    },
    data() {
    return {
      email: null,
      auth_token: null,
      searchresults: {},
      error: "",
      good: "",
      s: null
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
  },
  methods: {
    
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
                router.go(-1);
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
                router.go(-1);
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
    storeData(user_id){
      localStorage.setItem("user_id",user_id)
    },
    
    async search(){
        return fetch(`http://127.0.0.1:5000/api/search/${this.email}/${this.s}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authentication-Token": `${this.auth_token}`
                },
                }).then((response) => response.json())
                .then((data) => {
                this.searchresults=data
                console.log(data)
                }).catch((error) => console.log("1st", error))
            },
    async store(profile_id){
        localStorage.setItem("profile_id", profile_id)
    }
    }
}
</script>

<style scoped>

/* .all{
    position: relative;

} */
.search{
    /* border: 1px solid red; */
    float: right;
    width: 1067px;
    min-height: 98vh;
    padding: 5%;
    background: url(../assets/ab.jpg);
    background-position: center;
    background-size: cover;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}

.s_bar{
    border: 3px solid rebeccapurple;
    top: 100px;
    width: 100%;
    max-width: 700px;
    background: wheat;
    display: flex;
    align-items: center;
    border-radius: 60px;
    padding: 0px 0px;
    position: absolute;
    justify-content: center;
    left: 200px;
}

.s_bar input{
    border: 0;
    background: transparent;
    outline: none;
    padding: 24px 20px;
    font-size: 20px;
    color: black;
    width: 610px;
}

::placeholder{
    color: black;
}

.s_bar button{
    border: 0;
    border-radius: 50%;
    width: 60px;
    height: 60px;
    background: transparent;
    cursor: pointer;
}

.res{
    /* border: 1px solid red; */
    padding: 10px 20px;
    margin-top:0px;
    margin-right: 600px;
    width: 600px;
    position: absolute;
    left: 250px;
    top: 200px;
    font-weight: bold;
    font-size: 1.6rem;
}

.s_name{
    /* border: 1px solid rebeccapurple; */
    margin: 15px;
    height: 40px;
    position: relative;
    /* text-align: left; */
}

/* .s_name a{
    border: 1px solid green;
    display: inline;
    position: absolute;
    margin-right: 10px;
    left: 0px;
    width:100%;
} */

#un{
    position: absolute;
    /* border: 1px solid red; */
    left: 0px;
    font-size: 1.8rem;
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

/* #unf{
    right: 5px;
    position: absolute;
}

#f{
    right: 110px;
    position: absolute;
    left:200px;
    float:right;
} */

/* .s_name a button{
    border: 1px solid red;
    font-weight: bold;
    font-size: 1.3rem;
    padding: 4px;
     */

</style>
