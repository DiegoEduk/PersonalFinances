<template>
    <!-- Sidebar -->
    <ul class="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion" id="accordionSidebar">

        <!-- Sidebar - Brand -->
        <div class="sidebar-brand d-flex align-items-center justify-content-center">
            <div class="sidebar-brand-icon rotate-n-15">
                <i class="fas fa-laugh-wink"></i>
            </div>
            <div class="sidebar-brand-text mx-3">Personal Finances</div>
        </div>

        <!-- Divider -->
        <hr class="sidebar-divider my-0">

        <!-- Nav Item - Dashboard -->
        <li class="nav-item">
            <a class="nav-link" href="index.html">
                <i class="fas fa-fw fa-tachometer-alt"></i>
                <span>Transacciones</span></a>
        </li>

    </ul>
    <!-- End of Sidebar -->
</template>

<script>
import { defineComponent, toRefs } from 'vue';
import { useAuthStore } from '@/store/'; // Importa el store de autenticación

export default defineComponent({
    setup(_, { emit }) {
        const authStore = useAuthStore(); // Accede al store de autenticación
        const { permissions } = toRefs(authStore); // Desestructura y hace reactiva la propiedad permissions

        const selectComponent = (componentName) => {
            emit('component-selected', componentName); // Emite un evento para seleccionar el componente
        };

        return {
            permissions,
            selectComponent
        };
    }
});
</script>