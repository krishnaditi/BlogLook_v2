<template>
    <SideBar />
    <div class="DeleteBlog" align="middle">
        <div style="text-align: center;
        position:relative;
        width : 1050px; font-size: 3rem;
        left: 150px; top: 150px;">
        <h2>
            <p>Are you sure you want </p>
            to delete blog?
        </h2>
    </div>

    <div style="position:relative;
        width : 1050px; font-size: 3rem;
        left: 150px; top: 200px;">

        <button id = "fl" @click="deleteBlog" 
        style="height: 70px; width: 100px; font-size: 1.5rem; 
        font-weight:bold; 
        border: 2px solid green;">
        YES
        </button> 
        &nbsp; &nbsp;

        <router-link to="/userfeed">
            <button id = "uf" style="height: 70px; width: 100px;
            font-weight:bold;  
            font-size: 1.5rem; border: 2px solid red;">
            NO
            </button>
        </router-link>
</div>
    </div>
</template>
<script>
import SideBar from './SideBar.vue';
    export default {
        name: 'DeleteBlog',
        components: {
            SideBar
        },
        data() {
            return {
                user_id:null,
                error: "",
                auth_token: null,
                email: null,
                post_id:null
            };
        },
        async created() {
            this.post_id = localStorage.getItem("post_id");
            this.auth_token = sessionStorage.getItem("auth-token")
            if(!this.auth_token){
                alert("Login to view your Dashboard")
                this.$router.push("/")
            }
            this.email = sessionStorage.getItem("email")
            console.log(this.listid);
        },
        methods:{
            async deleteBlog(){
            try{
                fetch(`http://127.0.0.1:5000/api/blog/${this.email}/${this.post_id}`,{
                    method: "DELETE",
                    headers:{
                        "Content-Type" : "application/json",
                        "Authentication-Token":`${this.auth_token}`
                    }
                })
                .then((resp) =>  resp.json())
                .then((data) => {
                    const response = data;
                    console.log(response)
                    if (response.message) {
                        this.error = response.message;
                        console.log(response.message);
                    } else {
                        console.log("Post Deleted");}
                        this.$router.push("myprofile");
                    }).catch((error) => {
                        console.log("1st",error);
                    });
                }catch(error){
                    console.log("2nd",error)
                }
            },
        },
    };
</script>

<style scoped>

#fl:hover{
    background: green;
    color: white;
    cursor: pointer;
    border: 2px solid black;
}

#uf:hover{
    background: red;
    color: white;
    cursor: pointer;
    border: 2px solid black;
}

</style>