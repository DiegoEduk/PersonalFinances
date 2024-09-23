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
import TransactionCrud from '../components/Transaction/transactionsCrud.vue';
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
        TransactionCrud: markRaw(TransactionCrud),
        CategoryCrud: markRaw(CategoryCrud),
    },
    data() {
        return {
            // Define el componente que se mostrará inicialmente
            currentComponent: TransactionCrud
        };
    },
    methods: {
    changeComponent(componentName) {
      // Mapea nombres a componentes
      const componentMap = {
        BlankPage: BlankPage,
        ListUsers: ListUsers,
        TransactionCrud: TransactionCrud,
        CategoryCrud: CategoryCrud,
        // otros componentes
      };
      // Cambia el componente actual
      this.currentComponent = componentMap[componentName] || BlankPage;
    }
  }
}
</script>
