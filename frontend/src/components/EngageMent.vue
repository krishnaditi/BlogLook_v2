<template>
    <div class="summary">
      <SideBar />
        <p class="alert alert-danger" v-if="error" align="middle">{{ error }}</p>
        <p class="alert alert-success" v-if="good" align="middle">{{ good }}</p>
        <h3 align="left">Welcome {{ this.u.username }}</h3>
        <h4 style="text-align: center; position: relative; margin-right: 100px; left: 100px;">Total Posts {{ this.u.total_posts }} | Followers Count {{ this.u.followers }} | Following Count {{ this.u.following }}</h4>
        <img :src="`data:image/png;base64,${value_}`" alt="image not found" 
        style="height: 550px; width:600px; text-align: center;
        position: relative; margin-right: 100px; left: 100px;"/>
    </div>
</template>

<script>
import SideBar from './SideBar.vue';
    export default {
    name: "SummaryPg",
    components: {
      SideBar
    },
    data() {
    return {
      u: {},
      email: null,
      auth_token: null,
      value_: null,
      error: "",
      good: ""
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
    return fetch(`http://127.0.0.1:5000/api/engagement/${this.email}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": `${this.auth_token}`
      }
    }).then((response) => response.json())
    .then((data) => {
      this.u=data[0]
      this.value_ = data[1]
      console.log(data)
    }).catch((error) => console.log("1st", error))
  },
  };
</script>
