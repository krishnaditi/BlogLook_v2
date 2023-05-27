<template>
    <div class="addblo">
        <SideBar dp = "..." user_name = "Aadiu" full_name = "AK"/>
        <AddBlog />
    </div>
</template>

<script>

import SideBar from "@/components/SideBar.vue"

import AddBlog from "@/components/AddBlog.vue"

export default {
    name: 'AddBlo',
    components: {
        SideBar,
        AddBlog
    }
}
</script>