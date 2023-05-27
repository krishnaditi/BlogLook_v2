<template>
  <div class="about">
    <!-- <h1>This is an about page</h1> -->
    <SideBar dp = "..." user_name = "Aadiu" full_name = "AK"/>
    <!-- <UFeed posts /> -->
  </div>
</template>

<script>

import SideBar from '@/components/SideBar.vue'

// import UFeed from '@/components/UFeed.vue'

export default {
  name: 'UserFeed',
  components: {
    SideBar
    // UFeed
  }
}

</script>

