<template>
    <div class="form-group">
        <label for="rolesSelect">Seleccione un rol</label>
        <select class="form-control" id="rolesSelect" v-model="selectedRole" @change="updateRole">
            <option v-for="role in roles" :key="role.rol_name" :value="role.rol_name">
                {{ role.rol_name }}
            </option>
        </select>
    </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import { getAllRoles } from '@/services/roleServices';

export default {
    props: {
        selectedRole: {
            type: String,
            default: null,
        },
    },
    setup(props, { emit }) {
        const roles = ref([]);
        const selectedRole = ref(props.selectedRole);

        // Obtener roles de la API
        const fetchRoles = async () => {
            try {
                const response = await getAllRoles();
                roles.value = response.data;
            } catch (error) {
                console.error('Error al obtener los roles:', error);
            }
        };

        // Emitir el evento role-selected cuando cambie selectedRole
        const updateRole = () => {
            emit('role-selected', selectedRole.value);
        };

        // Obtener roles cuando el componente se monta
        onMounted(fetchRoles);

        // Usar watchEffect para observar y sincronizar selectedRole con props.selectedRole
        watchEffect(() => {
            if (selectedRole.value !== props.selectedRole) {
                selectedRole.value = props.selectedRole;
            }
        });

        return {
            roles,
            selectedRole,
            updateRole,
        };
    },
};
</script>

<style scoped>
/* Estilos opcionales */
</style>
