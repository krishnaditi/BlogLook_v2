import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../components/HomePage.vue'
import SideBar from '../components/SideBar.vue'
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage
  },

  {
    path: '/sidebar',
    name: 'sidebar',
    component: SideBar
  },

  {
    path: '/login',
    name: 'login',
    component: () => import( '../components/LoginPage.vue')

  },

  {
    path: '/signup',
    name: 'signup',
    component: () => import( '../components/SignUp.vue')

  },

  {
    path: '/userfeed',
    name: 'userfeed',
    component: () => import( '../components/UserFeed.vue')

  },

  {
    path: '/myprofile',
    name: 'myprofile',
    component: () => import( '../components/MyProfile.vue')

  },

  {
    path: '/Add_Blogs',
    name: 'Add_Blogs',
    component: () => import( '../components/Add_Blogs.vue')

  },

  {
    path: '/engagement',
    name: 'engagement',
    component: () => import( '../components/EngageMent.vue')

  },

  {
    path: '/search',
    name: 'search',
    component: () => import( '../components/SearchBar.vue')
  },

  {
    path: '/delete',
    name: 'delete',
    component: () => import( '../components/DeleteUser.vue')
  },

  {
    path: '/deletepost',
    name: 'deletepost',
    component: () => import( '../components/DeleteBlog.vue')
  },

  {
    path: '/updatepost',
    name: 'updatepost',
    component : () => import( '../components/UpdatePost.vue')
  },

  {
    path: '/deleteuser',
    name: 'deleteuser',
    component: () => import( '../components/DeleteUser.vue')
  },

  {
    path: '/otherprofile',
    name: 'otherprofile',
    component: () => import( '../components/OtherProfile.vue')
  },

  {
    path: '/followers',
    name: 'followers',
    component: () => import( '../components/FollowersPg.vue')

  },

  {
    path: '/following',
    name: 'following',
    component: () => import( '../components/FollowingPg.vue')

  },

  {
    path: '/updateprofile',
    name: 'updateprofile',
    component: () => import( '../components/UpdateProfile.vue')
  }


]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
