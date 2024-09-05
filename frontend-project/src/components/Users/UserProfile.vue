<!-- src/components/Users/UserProfile.vue -->
<template>
    <div>
        <h1>Perfil del Usuario</h1>
        <p><strong>Nombre:</strong> {{ user?.full_name }}</p>
        <p><strong>Email:</strong> {{ user?.mail }}</p>
        <p><strong>Rol:</strong> {{ user?.user_role }}</p>
        <button @click="logout">Cerrar sesión</button>
        <div v-for="permission in permissions" :key="permission.module_name">
            <!-- Muestra el nombre del módulo y su valor p_select -->
            <p>{{ permission.module_name }}: {{ permission.p_select }}</p>


        </div>
    </div>
</template>

<script>
import { useAuthStore } from '@/store'; // Importa el store de autenticación
import { useRouter } from 'vue-router'; // Importa Vue Router para la redirección

export default {
    setup() {
        const authStore = useAuthStore(); // Obtén la instancia del store
        const router = useRouter(); // Obtén la instancia del router

        // Propiedades para acceder a los datos del store
        const user = authStore.user;
        const permissions = authStore.permissions;


        // Acción para cerrar sesión
        const logout = () => {
            authStore.logout(); // Llama a la acción de logout del store
            router.push('/'); // Redirige a la ruta raíz
        };

        return {
            user,
            permissions,
            logout
        };
    }
};
</script>

<style>
/* Agrega estilos según sea necesario */
</style>