<script setup>
import BlankPage from '../components/Dashboard/BlankPage.vue';
import FooterCom from '../components/Dashboard/FooterCom.vue';
import Sidebar from '../components/Dashboard/Sidebar.vue';
import Topbar from '../components/Dashboard/Topbar.vue';
</script>

<template>
    <!-- Page Wrapper -->
    <div id="wrapper">
        <Sidebar />
        <!-- Content Wrapper -->
        <div id="content-wrapper" class="d-flex flex-column">
            <!-- Main Content -->
            <div id="content">
                <Topbar />
                <BlankPage />
            </div>
            <FooterCom />
        </div>
    </div>
</template>