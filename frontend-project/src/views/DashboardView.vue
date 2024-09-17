<template>
    <!-- Page Wrapper -->
    <div id="wrapper">
        <!-- Componente Sidebar que emite el evento para seleccionar el componente -->
        <Sidebar @component-selected="changeComponent" />
        <!-- Content Wrapper -->
        <div id="content-wrapper" class="d-flex flex-column">
            <!-- Main Content -->
            <div id="content">
                <Topbar />
                <!-- Componente Content que muestra el componente dinámico -->
                <DynamicComponent :currentComponent="currentComponent" />
            </div>
            <FooterCom />
        </div>
    </div>
</template>

<script>
import { markRaw } from 'vue'; // La función markRaw se usa para marcar un objeto como no reactivo. 
import DynamicComponent from '../components/Dashboard/DynamicComponent.vue';
import BlankPage from '../components/Dashboard/BlankPage.vue';
import FooterCom from '../components/Dashboard/FooterCom.vue';
import Sidebar from '../components/Dashboard/Sidebar.vue';
import Topbar from '../components/Dashboard/Topbar.vue';
import BlankPage01 from '../components/Dashboard/BlankPage01.vue';
import BlankPage02 from '../components/Dashboard/BlankPage02.vue';
import ListUsers from '../components/Users/ListUsers.vue';
import CategoryCrud from '../components/Category/CategoryCrud.vue';

export default {
    components: {
        DynamicComponent, // Registra el componente dinámico
        BlankPage: markRaw(BlankPage),
        FooterCom: markRaw(FooterCom),
        Sidebar: markRaw(Sidebar),
        Topbar: markRaw(Topbar),
        ListUsers: markRaw(ListUsers),
        BlankPage02: markRaw(BlankPage02),
        BlankPage02: markRaw(BlankPage02),
        CategoryCrud: markRaw(CategoryCrud),
    },
    data() {
        return {
            // Define el componente que se mostrará inicialmente
            currentComponent: BlankPage
        };
    },
    methods: {
    changeComponent(componentName) {
      // Mapea nombres a componentes
      const componentMap = {
        BlankPage: BlankPage,
        ListUsers: ListUsers,
        BlankPage02: BlankPage02,
        CategoryCrud: CategoryCrud,
        // otros componentes
      };
      // Cambia el componente actual
      this.currentComponent = componentMap[componentName] || BlankPage;
    }
  }
}
</script>
