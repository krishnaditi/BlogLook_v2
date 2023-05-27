<template>
    <div class="homie">
        <header>
        <div class="main">
            <div class="logo">
                <img src="../assets/logo.jpg">
            </div>
            <ul>
                <li class="active"><a href="/">Home</a></li>
                <li><a href="/login">Login</a></li>
                <li><a href="/signup">Signup</a></li>
            </ul>
        </div>
        <div class="title">
            <h1>BLOG-LOOK</h1>
            <h3>Blogging is not rocket science. 
                It's about being yourself and putting what 
                <p>you have into it.</p></h3>
        </div>

        <div class="button">
            <a href="/login" class="btn">Login</a>
            <a href="/signup" class="btn">Signup</a>
        </div>
</header>
    </div>
</template>

<script>
export default {
  name: 'HomePage'
}
</script>

<style scoped>

*{
    margin: 0;
    padding: 0;
    font-family: Arial, Helvetica, sans-serif;
}

header{
    background: url(../assets/home.jpg);
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

.title{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.title h1{
    color: black;
    text-align: center;
    padding: 10px;
    text-shadow: grey 3px 3px 6px;
    font-size: 2rem;
}

.title h3{
    color: black;
    padding: 20px;
    font-size: 1.6rem;
    text-align: center;
    font-style: italic;
    text-shadow: grey 3px 3px 6px;
}

.button{
    position: absolute;
    top: 70%;
    left: 50%;
    transform: translate(-50%, -50%); 
}

.btn{
    font-weight: bold;
    border: 5px solid black;
    padding: 10px 30px;
    color: black;
    text-decoration: none;
    transition: 0.6s ease;
    margin-left: 3px;
    background-color: aqua;
}

.btn:hover{
    background-color: black;
    color: wheat;
}

</style>