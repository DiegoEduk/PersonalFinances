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
        <hr class="sidebar-divider mb-4">

        <div v-for="permission in permissions" :key="permission.module_name">

            <!-- Botón para acceder al módulo si tiene permisos -->
            <li class="nav-item" v-if="permission.p_select && permission.module_name == 'usuarios' ">
                <button class="btn btn-link text-white" @click="selectComponent('ListUsers')">
                    <i class="fa-solid fa-user">&nbsp;</i>
                    <span class="text-capitalize">{{ permission.module_name }}</span>
                </button>
            </li>

            <li class="nav-item" v-if="permission.p_select && permission.module_name == 'transacciones' ">
                <button class="btn btn-link text-white" @click="selectComponent('BlankPage02')">
                    <i class="fa-solid fa-money-check-dollar">&nbsp;</i>
                    <span class="text-capitalize">{{ permission.module_name }}</span>
                </button>
            </li>

            <li class="nav-item" v-if="permission.p_select && permission.module_name == 'categorias' ">
                <button class="btn btn-link text-white" @click="selectComponent('CategoryCrud')">
                    <i class="fa-solid fa-list">&nbsp;</i>
                    <span class="text-capitalize">{{ permission.module_name }}</span>
                </button>
            </li>

        </div>

        <!-- Divider -->
        <hr class="sidebar-divider">

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