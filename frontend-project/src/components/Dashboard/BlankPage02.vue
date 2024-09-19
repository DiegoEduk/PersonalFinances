<!-- BlankPage.vue -->
<template>
    <!-- Begin Page Content -->
    <div class="container-fluid">

        <!-- Page Heading -->
        <h1 class="h3 mb-4 text-gray-800">Blank Page 02</h1>
        <CategorySelect />
    </div>
    <!-- /.container-fluid -->
</template>


<script>
import CategorySelect from '../Category/CategorySelect.vue';

export default {
    name: 'BlankPage02',
    components: {
        CategorySelect, 
    },
};
</script>