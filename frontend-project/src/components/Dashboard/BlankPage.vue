<!-- BlankPage.vue -->
<template>
    <!-- Begin Page Content -->
    <div class="container-fluid">

        <!-- Page Heading -->
        <h1 class="h3 mb-4 text-gray-800">Blank Page</h1>
        <RolesSelect />

    </div>
    <!-- /.container-fluid -->
</template>


<script>
import RolesSelect from '../Roles/RolesSelect.vue';

export default {
    name: 'BlankPage',
    components: {
        RolesSelect, // Incluir el spinner global
    },
};
</script>