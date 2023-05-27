<template>
    <div class="editblo">
        <SideBar dp = "..." user_name = "Aadiu" full_name = "AK"/>
        <EditBlog />
    </div>
</template>

<script>

import SideBar from "@/components/SideBar.vue"

import EditBlog from "@/components/EditBlog.vue"

export default {
    name: 'EditBlo',
    components: {
        SideBar,
        EditBlog
    }
}

</script>