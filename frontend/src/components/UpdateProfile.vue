<template>
    <div class="up">
        <SideBar/>

        <div class="edit">
            <p align="middle" class="alert alert-danger" v-if="error">{{ error }}</p>
            <p align="middle" class="alert alert-success" v-if="good">{{ good }}</p>
            <div class="e_profile">
                <h1>Edit Your Profile</h1>
                <form action="http://127.0.0.1:5000/editprofile/{{ user_id }}" method='POST' enctype="multipart/form-data">
                    <label>Enter your full name</label>
                    <br> 
                    <input type="text" name="fullname" v-model="nfullname">
                    <br>
                    <label>Give a description about yourself</label>
                    <input type="text" name="about" v-model="nabout" id="desc">
                    <br>
                    <label>Upload your profile picture</label>
                    <input ref = "image_input" type="file" name="image" @input = "image_upload()"/>
                    <br>
                    <input type="submit" @click.prevent="update()" value="Update Profile" id="u_profile">  
                </form>
            </div>
        </div>
    </div>
</template>


<script>
import SideBar from './SideBar.vue';
    export default {
    name: "UpdateProfile",
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
        nfullname: "",
        nabout: "",
        p_img: "",
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
        async image_upload() {
        let img = this.$refs.image_input.files;
        this.p_img = img[0];
        console.log(img[0])
        },

        async update() {

            let f_data = new FormData();
            f_data.append('fullname', this.nfullname);
            f_data.append('about', this.nabout);
            f_data.append('p_image', this.p_img);
            f_data.append('email', this.email);
            if(!this.nfullname) {
                this.nfullname = localStorage.getItem('fullname');
            }
            else if(!this.nabout) {
                this.nabout = localStorage.getItem('about');
            }
            else {
                try {
                    fetch("http://127.0.0.1:5000/api/user/"+`${this.email}`, {
                        method: "PUT",
                        headers: {
                            "Authentication-Token": `${this.auth_token}`,
                        },
                        body: f_data,
                        })
                        .then((resp) =>  resp.json())
                        .then((data) => {
                            const response = data;
                            if (response.message) {
                                this.error = response.message;
                                console.log(response.message);
                            } else {
                                this.lists = data;
                                console.log(this.lists);
                                console.log("Profile Updated");
                                this.$router.push("userfeed");
                                console.log("its userfeed returns");
                            }
                        })
                        .catch((error) => {
                            console.log("1st",error);
                        });
                    } catch (error) {
                        console.log("2nd",error);
                    }
                }
        }
    }
}
</script>

<style scoped>

.edit{
    /* border: 1px solid red; */
    min-height:100vh ;
    background-size: cover; 
    position: relative;
    background-position: center;
    position:relative;
    width : 1050px;
    left: 300px;
}

.e_profile{
    position: absolute;
    width: 450px;
    background: url(../assets/h1.jpg) no-repeat center/cover;
    min-height: 450px;
    margin-left: 300px;
    /* border:1px solid red; */
    top: 80px;
    display:absolute;
    font-size: large;
    font-weight: bold;
    box-shadow: 10px 10px 20px rgb(1, 74, 219);
}

.e_profile h1{
    margin: 5px;
    font-size:2rem;
    text-decoration: underline;
    color: wheat;
    text-align: center;
}

.e_profile form{
    color:white;
    /* border: 1px solid red; */
    font-size: 1.4rem;
    margin: 15px;
    padding: 30px;
    justify-content: center;
    text-align: center;
    min-height: 400px;
}

.e_profile input{
    margin: 20px;
    width: 150px;
    height: 30px;
    font-size: 0.9rem;
}

#desc{
    width:250px;
    height: 40px;

}

#u_profile{
    font-weight: bold;
    font-size: 1.2rem;
    background-color: rgb(180, 180, 180);

}

#u_profile:hover{

    background-color: wheat;
    cursor: pointer;
    box-shadow: 2px 2px 5px wheat;
}

</style>