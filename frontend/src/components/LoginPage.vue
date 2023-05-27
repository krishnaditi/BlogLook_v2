<template>
    <div class="loginpage">
        <header>
            <div class="main">
                <div class="logo">
                    <img src="../assets/logo.jpg">
                </div>
                <ul>
                    <li><router-link to="/">Home</router-link></li>
                    <li class="active"><router-link to = "/login">Login</router-link></li>
                    <li><router-link to = "/signup">Signup</router-link></li>
                </ul>
            </div>
        </header>

        <!-- Error Handling -->
        <div align="middle">
            <p class="alert alert-danger" v-if="error_1">{{ error_1 }}</p>
            <p class="alert alert-danger" v-if="error_2">{{ error_2 }}</p>
        </div>

        <!-- Login-Page -->
        <div class = "center">
        <h1>Login</h1>

        <!-- E-mail -->
            <div class="txt_field">
                <input type="email"
                id = "email"
                name = "email" 
                v-model="email"
                style = "width: 300px; text-align: center;" 
                required>
                <label>Email ID</label>
            </div> 

        <!-- Password -->
            <div class="txt_field">
                <input  type = "password" 
                id = "password"
                name = "password"
                v-model="password" 
                minlength="8" 
                title="Password requires atleast 8 characters." 
                pattern=".{8,}"
                style = "width: 300px; text-align: center;"
                required>
            <label>Password</label>
            </div>
            
        <!-- submit button -->
            <div class="signup_link" align = "center">
                <input type="submit" @click="login" value="Login">
                <br><br>
                <p>Don't have an account?
                    <router-link to="/signup">Sign-Up</router-link>
                </p>
            </div>
        </div>
    </div>    
</template>

<script>
export default {
    name:'LoginPage',
    data() {
        return {
            email: null,
            password: null,
            error_1: "",
            error_2: "",
            auth: null,
            is_authenticated: false
        }
    },
    async created() {
        sessionStorage.clear()
        localStorage.clear()
    },
    async updated() {
        sessionStorage.clear()
        localStorage.clear()
        },
    methods:{
        async login() {
            try {
                fetch("http://127.0.0.1:5000/login?include_auth_token",{
                    method: "POST",
                    headers: {
                        "Access-Control-Allow-Origin": "*",
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        email: this.email, password: this.password, is_authenticated: true
                    })
                }).then((resp) => resp.json())
                .then(async (data) =>{
                    const { response } = data;
                    console.log(data);
                    if (response.errors) {
                        if (response.errors[1]) {
                            this.error_1 = response.errors[1];
                            alert(this.error_1)
                        }
                        this.error_2 = response.errors[0];
                        alert(this.error_2)
                        console.log(this.error_1, this.error_2);
                    } 
                    else {
                        this.auth = response.user.authentication_token;
                        sessionStorage.setItem("auth-token", this.auth);
                        sessionStorage.setItem("email", this.email);
                        this.$router.push("userfeed");
                        console.log("its homepage");
                    }
                })
                .catch((error) => {
                    console.log("some error first time",error)
                    alert(error)
                })
            } 
            catch(error){
                console.log("No way home: ", error)
                alert(error)
            }
        }
    }
}
</script>

<style scoped>
*{
    margin: 0;
    padding: 0;
    font-family: Arial, Helvetica, sans-serif;
}

header{
    background-image: url(../assets/home.jpg);
    height: 100vh;
    background-size: cover;
    background-position: center;
}

ul{
    float: right;
    list-style-type: none;
    margin-top: 25px;
}

ul li{
    display: inline-block;
}

ul li a{
    font-weight: bold;
    text-decoration: none;
    color: black;
    padding: 5px 20px;
    border: 1px solid transparent;
    transition: 0.6s ease;
    border: 3px solid black;
    margin-left: 3px;
    background-color: aqua;
}

ul li a:hover{
    background-color: black;
    color: wheat;
}

ul li.active a{
    background-color: black;
    color: wheat;
}

.logo{
    position: absolute;
    left: -10px;
    /* border: 5px solid #05f7ff; */
}

.logo img{
    float: left;
    width: 80px;
    height: auto;
}

.main{
    max-width: 1200px;
    margin: auto;
}

body{
    margin: 0;
    padding: 0;
    font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    height: 100vh;
    overflow: hidden;
}

.center{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 400px;
    background: white;
    border-radius: 10px;
    padding: 30px;
    border: black 5px solid;
    box-shadow: grey 2px 2px 7px 7px;
}

.center h1{
    text-align: center;
    padding: 20px 20px 20px 20px;
    border-bottom: 2px solid black;
}
.center form{
    padding:  0 40px;
    box-sizing: border-box;
}

.center .txt_field{
    position: relative;
    border-bottom: 2px solid #adadad;
    margin: 30px 0;
}

.txt_field input{
    width: 100%;
    padding: 0 5px;
    height: 40px;
    font-size: 16px;
    border: none;
    background: none;
    outline: none;
}

.txt_field label{
    position: absolute;
    top: 50%;
    left: 35px;
    color: #adadad;
    transform: translate(-50%, -50%);
    font-size: 16px;
    pointer-events: none;
    transition: .5s;
}

.txt_field span::before{
    content: '';
    position: absolute;
    top: 40px;
    left: 0;
    width: 100%;
    height: 2px;
    background: #2691d9;
    transition: .5s;
}

.txt_field input:focus ~ label,
.txt_field input:valid ~ label{
    top: -5px;
    color: #2691d9;
    text-align: center;
}

.txt_field input:focus ~ span::before,
.txt_field input:valid ~ span::before{
    width: 100%;
}

input[type="submit"]{
    width: 100%;
    height: 50px;
    border: 1px solid;
    background: #2691d9;
    border-radius: 25px;
    font-size: 18px;
    color: #e9f4fb;
    font-weight: 700;
    cursor: pointer;
    outline: none;
    border: black 2px solid;
}

input[type="submit"]:hover{
    background: aqua;
    color: black;
    transition: .5s;
}

.signup_link{
    margin: 30px;
    text-align: center;
    font-size: 16px;
    color: #666666;
}

.signup_link a{
    color: #2691d9;
    text-decoration: none;
}

.signup_link a:hover{
    text-decoration: underline;
}

</style>