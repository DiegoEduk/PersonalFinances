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
                                <td>{{ user.img_profile }} - {{ user.full_name }}</td>
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
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <!-- Título cambia según el modo (crear o editar) -->
            <h5 class="modal-title" id="userModalLabel">{{ isEditMode ? 'Editar Usuario' : 'Registrar Usuario' }}</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <div class="row">
                <div class="col-sm-6">
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
                            <RolesSelect :selectedRole="currentUser.user_role" @role-selected="updateUserRole" />
                        </div>
                        <!-- Campo para la contraseña, v-if hace que solo se muestra en el modo de crear usuario  -->
                        <div class="mb-3" v-if="!isEditMode">
                            <label for="userPassword" class="form-label">Contraseña</label>
                            <input type="password" id="userPassword" class="form-control" v-model="currentUser.passhash" required>
                        </div>
                        <!-- Campo para cargar la imagen -->
                        <div class="form-group">
                            <label for="imageUpload"  class="form-label">Cargar Imagen:</label>
                            <input type="file" id="imageUpload" class="form-control" @change="onImageChange" accept="image/*" />
                        </div>
                        <!-- Botón de enviar (guardar o registrar) según isEditMode -->
                        <button type="submit" class="btn btn-primary">{{ isEditMode ? 'Guardar Cambios' : 'Registrar Usuario' }}</button>
                    </form>
                </div>
                <div class="col-sm-6">
                    <div class="m-3">
                        <!-- Aquí cargar visualizar imagen -->
                        <img v-if="imagePreview" :src="imagePreview" alt="Previsualización de imagen" class="img-fluid" />
                        <img v-if="currentUser && currentUser.img_profile" :src="`${apiUrl}${currentUser.img_profile}`" alt="Profile Image" />
                        <!-- Alternativa si no hay imagen disponible -->
                        <p v-else>No hay imagen disponible</p>
                    </div>  
                </div>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
// Importar los metodos del archivo /services/userService para hacer pediticones a la API
import { getUsersByPage, deleteUser, updateUser, createUser } from '@/services/userService';
import RolesSelect from '../Roles/RolesSelect.vue';

export default {
    data() {
        return {
            users: [],  // Lista de usuarios
            currentUser: {},  // Usuario actual para crear o editar
            currentPage: 1,  // Página actual para la paginación
            totalPages: 0,  // Total de páginas
            isEditMode: false,  // Indica si estamos en modo edición o creación
            apiUrl: import.meta.env.VITE_API_URL, // Tomar la URL base de la variable de entorno
            
            imageFile: '',
            imagePreview: '',
        }
    },
    components: {
        RolesSelect, // Registra el componente
    },
    methods: {
        // Obtiene los usuarios de la página actual
        async fetchUsers() {
            try {
                const response = await getUsersByPage(this.currentPage);
                this.users = response.data.users; // Asigna los usuarios obtenidos
                this.totalPages = response.data.total_pages; // Asigna el total de páginas
            } catch (error) {
                // Imprime el error 
                alert(error.data.detail);
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
                    // Imprime el error 
                    alert(error.data.detail);
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
            console.log(this.currentUser.img_profile);
            this.isEditMode = true; // Cambia el modo a editar a verdadero
            $('#userModal').modal('show'); // Abre el modal
        },

        // Actualizamos el rol seleccionado en `currentUser`
        updateUserRole(selectedRole) {
            this.currentUser.user_role = selectedRole;
        },

        // Registra un nuevo usuario llamando a la API
        async registerUser() {
            try {
                // Usa la función createUser (llamando a la API) para crear un nuevo usuario 
                await createUser(this.currentUser.full_name, this.currentUser.mail, this.currentUser.user_role, this.currentUser.passhash, this.imageFile);
                alert('Usuario registrado exitosamente');
                this.fetchUsers(); // Refresca la lista de usuarios después de registrar
                $('#userModal').modal('hide'); // Cierra el modal
            } catch (error) {
                // Imprime el error 
                alert(error.data.detail);
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
                // Imprime el error 
                alert(error.data.detail);
            }
        },

        onImageChange(event) {
            const file = event.target.files[0];
            if (file) {
                this.imageFile = file;
                this.imagePreview = URL.createObjectURL(file);
            }
        },
        

    }, // end-methods
    mounted() {
        this.fetchUsers(); // Llama al método para obtener al cargar este componente
    },
}
</script>