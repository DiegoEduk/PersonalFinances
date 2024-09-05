<template>
  <div class="container-fluid">

    <!-- Título de la página -->
    <h1 class="h3 mb-2 text-gray-800">Usuarios</h1>

    <!-- Botón para registrar un nuevo usuario -->
    <button @click="openCreateModal" class="btn btn-success mb-4">Registrar Usuario</button>

    <!-- Tarjeta que contiene la tabla de usuarios -->
    <div class="card shadow mb-4">
      <!-- Encabezado de la tarjeta -->
      <div class="card-header py-3">
        <h6 class="m-0 font-weight-bold text-primary">Lista de Usuarios</h6>
      </div>

      <!-- Cuerpo de la tarjeta -->
      <div class="card-body">
        <div class="table-responsive">
          <!-- Tabla para mostrar la lista de usuarios -->
          <table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Correo</th>
                <th>Rol</th>
                <th>Estado</th>
                <th>Última Actualización</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.user_id">
                <td>{{ user.full_name }}</td>
                <td>{{ user.mail }}</td>
                <td>{{ user.user_role }}</td>
                <td>{{ user.user_status ? 'Activo' : 'Inactivo' }}</td>
                <td>{{ formatDate(user.updated_at) }}</td>
                <td>
                  <button @click="openEditModal(user)" class="btn btn-warning btn-sm">Editar</button>
                  <button @click="deleteUser(user.user_id)" class="btn btn-danger btn-sm">Eliminar</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Controles de paginación -->
        <div class="pagination-controls">
          <div class="pagination-controls">
            <button class="btn btn-primary m-3" @click="prevPage" :disabled="currentPage === 1">Anterior</button>
            <span>Página {{ currentPage }} de {{ totalPages }}</span>
            <button class="btn btn-primary m-3" @click="nextPage"
              :disabled="currentPage === totalPages">Siguiente</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal para crear / editar usuario -->
    <div class="modal fade" id="userModal" tabindex="-1" aria-labelledby="userModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="userModalLabel">{{ isEditMode ? 'Editar Usuario' : 'Registrar Usuario' }}</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="isEditMode ? updateUser() : registerUser()">
              <div class="mb-3">
                <label for="userName" class="form-label">Nombre</label>
                <input type="text" id="userName" class="form-control" v-model="currentUser.full_name" required>
              </div>
              <div class="mb-3">
                <label for="userEmail" class="form-label">Correo</label>
                <input type="email" id="userEmail" class="form-control" v-model="currentUser.mail" required>
              </div>
              <div class="mb-3">
                <label for="userRole" class="form-label">Rol</label>
                <input type="text" id="userRole" class="form-control" v-model="currentUser.user_role" required>
              </div>
              <!-- Campo para la contraseña, solo se muestra en el modo de creación -->
              <div class="mb-3" v-if="!isEditMode">
                <label for="userPassword" class="form-label">Contraseña</label>
                <input type="password" id="userPassword" class="form-control" v-model="currentUser.passhash" required>
              </div>
              <button type="submit" class="btn btn-primary">{{ isEditMode ? 'Guardar Cambios' : 'Registrar Usuario'
                }}</button>
            </form>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
// Importa los servicios necesarios
import { getUsersByPage, deleteUser, updateUser, createUser } from '@/services/userService';

export default {
  data() {
    return {
      users: [],         // Arreglo para almacenar la lista de usuarios obtenidos
      currentUser: {},   // Usuario actualmente seleccionado para edición o creación
      currentPage: 1,    // Página actual de la paginación
      totalPages: 0,     // Total de páginas disponibles
      isEditMode: false, // Variable para determinar si estamos en modo edición o creación
    };
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await getUsersByPage(this.currentPage);
        this.users = response.data.users;
        this.totalPages = response.data.total_pages;
      } catch (error) {
        alert('Error al obtener los usuarios:', error);
      }
    },

    openCreateModal() {
      this.currentUser = { full_name: '', mail: '', user_role: '', passhash: '' }; // Inicializa el usuario vacío
      this.isEditMode = false;
      $('#userModal').modal('show'); // Abre el modal
    },

    openEditModal(user) {
      this.currentUser = { ...user }; // Clona el usuario seleccionado
      this.isEditMode = true;
      $('#userModal').modal('show'); // Abre el modal
    },

    async registerUser() {
      try {
        await createUser(this.currentUser.full_name, this.currentUser.mail, this.currentUser.user_role, this.currentUser.passhash);
        alert('Usuario registrado exitosamente');
        this.fetchUsers(); // Refresca la lista de usuarios después de registrar
        $('#userModal').modal('hide'); // Cierra el modal
      } catch (error) {
        alert('Error al registrar el usuario:', error);
      }
    },

    async updateUser() {
      try {
        await updateUser(this.currentUser.user_id, this.currentUser.full_name, this.currentUser.mail, this.currentUser.user_role);
        alert('Usuario actualizado exitosamente');
        this.fetchUsers(); // Refresca la lista de usuarios después de actualizar
        $('#userModal').modal('hide'); // Cierra el modal
      } catch (error) {
        alert('Error al actualizar el usuario:', error);
      }
    },

    async deleteUser(userId) {
      if (confirm('¿Estás seguro de que deseas eliminar este usuario?')) {
        try {
          await deleteUser(userId);
          alert('Usuario eliminado exitosamente');
          this.fetchUsers(); // Refresca la lista de usuarios después de eliminar
        } catch (error) {
          alert('Error al eliminar el usuario:', error);
        }
      }
    },

    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
        this.fetchUsers();
      }
    },

    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.fetchUsers();
      }
    },

    formatDate(dateString) {
      const options = {
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      };
      return new Date(dateString).toLocaleDateString('es-ES', options);
    },
  },

  mounted() {
    this.fetchUsers(); // Llama al método para obtener los usuarios al cargar el componente
  },
};
</script>

<style scoped>
/* Estilos opcionales para mejorar la apariencia de los controles de paginación */
</style>
