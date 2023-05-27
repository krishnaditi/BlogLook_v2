<template>
    <div class="editpro">
        <SideBar dp = "..." user_name = "Aadiu" full_name = "AK"/>
        <EditProfile />
    </div>
</template>

<script>

import SideBar from "@/components/SideBar.vue"

import EditProfile from "@/components/EditProfile.vue"

export default {
    name : 'EditPro',
    components : {
        SideBar,
        EditProfile
    }
}

</script>