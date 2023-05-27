<template>
    <div class="ab">
        <SideBar />
        <div class="add_blog" style="border: 1px solid white;
            background: url(../assets/ab.jpg) no-repeat center/cover;
            position: relative; background-position: center;
            height: 99vh;">
            <br><br>

            <div align="middle">
                <p class="alert alert-danger" v-if="error">{{ error }}</p>
            </div>

            <p style="font-size:2rem;text-decoration: underline;
            color: black;font-weight: bold;
            text-align: center; height: 10px;">Add New Blog</p>
            <br><br><br><br>
            
            <form enctype = "multipart/form-data">

            <div class="Upload">
                <!-- name of the blog -->      
                <label>Heading of your Blog</label>
                <input type="text" name="heading" id="head" v-model="heading" required style="box-sizing: border-box;"/>
                <br><br>
            </div>

            <div class="Upload">
                <!-- describe -->
                <label>Description</label> 
                <input type="text" name="description" id="des" v-model="description"/>
                <br>
                <br>
            </div>
        
            <div class="Upload">
                <!-- image -->
                <label> Image Upload </label>
                <input ref = "image_input" type="file" name="b_image" style="cursor: pointer;" @input = "image_upload()"/>

                <div class="post_now">
                    <!-- submit -->
                    <router-link to="/myprofile"><input type="submit" @click="createBlog" value="Post Now"  id="upl"></router-link>
                </div>
            </div>
            </form>    
        </div>
    </div>
</template>
<script>
import SideBar from './SideBar.vue';
    export default {
        name: "Add_Blogs",
        components: {
            SideBar
        },
        data() {
            return {
                email: null,
                auth_token: null,
                error: "",
                heading: null,
                description: null,
                b_image: null
            };
        },
        mounted() {
            this.email=sessionStorage.getItem("email");
            this.auth_token=sessionStorage.getItem("auth-token");
            if(!this.auth_token){
                alert("Login to view your Dashboard")
                this.$router.push("/")
            }
        },
    methods: {
        
        async image_upload() {
        let img = this.$refs.image_input.files;
        this.b_image = img[0];
        console.log(img[0])
        
        },
        async createBlog() {
            console.log(this.b_image)
            let f_data = new FormData();
            f_data.append('heading', this.heading);
            f_data.append('description', this.description);
            f_data.append('b_image', this.b_image);
            f_data.append('email', this.email);
            if(!this.heading) {
                this.error = "Blog Heading can not be empty";
            }
            else {
                try {
                    fetch("http://127.0.0.1:5000/api/blog/"+`${this.email}`, {
                        method: "POST",
                        headers: {
                            // "Content-Type": "application/json;charset=utf-8",
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
                                console.log("Post Added");
                                this.$router.push("myprofile");
                                console.log("its profile returns");
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
    };
</script>

<style scoped>

.Upload{
    /* border: 1px solid red; */
    margin-top: 40px;
}

.add_blog{
    width: 1050px;
    float: right;
}

.add_blog form{
    margin-left: 100px;
    margin-right: 100px;
    margin-bottom: 400px;
}

.add_blog label{
    font-size: 1.3rem;
    font-weight: bold;
}

.add_blog input{
    box-sizing: border-box;
    border-color: blue;
    justify-content: center;
    text-align: center;
    cursor: auto;
    font-size: 1.4rem;
}

#head{
    width:400px;
    height: 60px;
}

#des{
    width:700px;
    height: 100px;
}

#upl{
    width: 100px;
    height: 30px;
    cursor: pointer;
    font-weight: bold;
}

#upl:hover{
    color: purple;
    background-color: wheat;
    font-weight: bold;
    box-sizing: border-box;
    box-shadow: 5px 5px 10px rgb(88, 88, 249);
}

.post_now{
    padding: 60px;
    text-align: center;
}

</style>
