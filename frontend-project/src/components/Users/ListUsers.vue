<!-- List Users -->
<template>
    <!-- Begin Page Content -->
    <div class="container-fluid">

        <!-- Título de la página -->
        <h1 class="h3 mb-2 text-gray-800">Usuarios</h1>

        <!-- Botón para registrar un nuevo usuario -->
        <button @click="openCreateModal" class="btn btn-success mb-4">Registrar Usuario</button>

        <!-- DataTales Example -->
        <div class="card shadow mb-4">
            <div class="card-header py-3">
                <h6 class="m-0 font-weight-bold text-primary">Lista de Usuarios</h6>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
                        <thead>
                            <tr>
                                <th>Nombre</th>
                                <th>Correo</th>
                                <th>Rol</th>
                                <th>Estado</th>
                                <th>Ultima Actualización</th>
                                <th></th>
                            </tr>
                        </thead>

                        <tbody>
                            <!-- Recorre la lista de usuarios con v-for -->
                            <tr v-for="user in users" :key="user.user_id">
                                <!-- Muestra los datos de cada usuario en cada td-->
                                <td>{{ user.full_name }}</td>
                                <td>{{ user.mail }}</td>
                                <td>{{ user.user_role }}</td>
                                <td>{{ user.user_status ? 'Activo' : 'Inactivo' }}</td>
                                <td>{{ formatDate(user.updated_at) }}</td>
                                <!-- Botones para editar o eliminar un usuario -->
                                <td>
                                    <button @click="openEditModal(user)" class="btn btn-outline-secondary"><i
                                            class="fa-solid fa-pen-to-square"></i></button>
                                    <button @click="deleteUserMethod(user.user_id)" class="btn btn-outline-dark"><i class="fa-solid fa-trash"></i></button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Controles de paginación -->
                <div class="pagination-controls">
                    <!-- Botón para la página anterior, con click llama a la función prevPage  -->
                    <button class="btn btn-primary m-3" @click="prevPage" :disabled="currentPage === 1">Anterior</button>
                    <!-- Muestra la página actual y total de páginas -->
                    <span>Página {{ currentPage }} de {{ totalPages }}</span>
                    <!-- Botón para la página siguiente,  con click llama a la función nextPage -->
                    <button class="btn btn-primary m-3" @click="nextPage" :disabled="currentPage === totalPages">Siguiente</button>
                </div>

            </div>
        </div>

    </div>
    <!-- /.container-fluid -->

    <!-- Modal para crear / editar usuario -->
    <div class="modal fade" id="userModal" tabindex="-1" aria-labelledby="userModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <!-- Título cambia según el modo (crear o editar) -->
            <h5 class="modal-title" id="userModalLabel">{{ isEditMode ? 'Editar Usuario' : 'Registrar Usuario' }}</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <!-- Formulario que llama a registerUser o updateUser según el modo isEditMode -->
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
              <!-- Campo para la contraseña, v-if hace que solo se muestra en el modo de crear usuario  -->
              <div class="mb-3" v-if="!isEditMode">
                <label for="userPassword" class="form-label">Contraseña</label>
                <input type="password" id="userPassword" class="form-control" v-model="currentUser.passhash" required>
              </div>
              <!-- Botón de enviar (guardar o registrar) según isEditMode -->
              <button type="submit" class="btn btn-primary">{{ isEditMode ? 'Guardar Cambios' : 'Registrar Usuario' }}</button>
            </form>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
// Importar los metodos del archivo /services/userService para hacer pediticones a la API
import { getUsersByPage, deleteUser, updateUser, createUser } from '@/services/userService';

export default {
    data() {
        return {
            users: [],  // Lista de usuarios
            currentUser: {},  // Usuario actual para crear o editar
            currentPage: 1,  // Página actual para la paginación
            totalPages: 0,  // Total de páginas
            isEditMode: false,  // Indica si estamos en modo edición o creación
        }
    },
    methods: {
        // Obtiene los usuarios de la página actual
        async fetchUsers() {
            try {
                const response = await getUsersByPage(this.currentPage);
                this.users = response.data.users; // Asigna los usuarios obtenidos
                this.totalPages = response.data.total_pages; // Asigna el total de páginas
            } catch (error) {
<<<<<<< HEAD
                this.handleError(error);
=======
                console.log(error);
>>>>>>> b95202f ( corrección editUser)
            }
        },

        // Función para ir a la página siguiente
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++; // incrementa el valor
                this.fetchUsers(); // Recarga la lista de usuarios para la nueva página
            }
        },

        // Función para ir a la página anteior
        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--; // disminuye el valor
                this.fetchUsers(); // Recarga la lista de usuarios para la nueva página
            }
        },

        // Formatea una fecha para mostrarla de manera legible
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

        // Elimina un usuario
        async deleteUserMethod(userId) {
            if (confirm('¿Estás seguro de que deseas eliminar este usuario?')) {
                try {
                    await deleteUser(userId); // Llama a la API para eliminar el usuario
                    alert('Usuario eliminado exitosamente');
                    this.fetchUsers(); // Refresca la lista de usuarios después de eliminar
                } catch (error) {
                    // Maneja el error utilizando un método auxiliar
<<<<<<< HEAD
                    this.handleError(error);
=======
                    alert(error.data.detail);
>>>>>>> b95202f ( corrección editUser)
                }
            }
        },

        // Abre el modal para registrar un nuevo usuario
        openCreateModal() {
            // Inicializa los campos vacios
            this.currentUser = { full_name: '', mail: '', user_role: '', passhash: '' }; // Inicializa el usuario vacío
            this.isEditMode = false; // Cambia el modo a editar a falso
            $('#userModal').modal('show'); // Abre el modal
        },

        // Abre el modal para editar un usuario
        openEditModal(user) {
            this.currentUser = { ...user }; // Clona el usuario seleccionado
            this.isEditMode = true; // Cambia el modo a editar a verdadero
            $('#userModal').modal('show'); // Abre el modal
        },

        // Registra un nuevo usuario llamando a la API
        async registerUser() {
            try {
                // Usa la función createUser (llamando a la API) para crear un nuevo usuario 
                await createUser(this.currentUser.full_name, this.currentUser.mail, this.currentUser.user_role, this.currentUser.passhash);
                alert('Usuario registrado exitosamente');
                this.fetchUsers(); // Refresca la lista de usuarios después de registrar
                $('#userModal').modal('hide'); // Cierra el modal
            } catch (error) {
                // Maneja el error utilizando un método auxiliar
<<<<<<< HEAD
                this.handleError(error);
=======
                alert(error.data.detail);
>>>>>>> b95202f ( corrección editUser)
            }
        },

        // Actualiza un usuario llamando a la API
        async updateUser() {
            try {
                await updateUser(this.currentUser.user_id, this.currentUser.full_name, this.currentUser.mail, this.currentUser.user_role);
                alert('Usuario actualizado exitosamente');
                this.fetchUsers(); // Refresca la lista de usuarios después de actualizar
                $('#userModal').modal('hide'); // Cierra el modal
            } catch (error) {
                // Maneja el error utilizando un método auxiliar
<<<<<<< HEAD
                this.handleError(error);
            }
        },

        // Para Manejar los errores de manera centralizada en este componente
        handleError(error) {
            // Si el BackEnd responde error
            console.log('Error:', error.response);
            if (error.response && error.response.data && error.response.data.detail) {
                alert(error.response.data.detail); // Muestra el mensaje de error
            } else {
                // Si es otro error, muestra un mensaje genérico si no hay detalle del error
                alert('Ocurrió un problema inesperado. Estamos trabajando para solucionarlo. Por favor, inténtalo más tarde.');
=======
                alert(error.data.detail);
>>>>>>> b95202f ( corrección editUser)
            }
        },

    }, // end-methods
    mounted() {
        this.fetchUsers(); // Llama al método para obtener al cargar este componente
    },
}
</script>