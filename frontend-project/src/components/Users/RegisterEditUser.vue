<template>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card shadow-lg my-5">
                    <div class="card-body">
                        <!-- Título dinámico que cambia según la acción (Registrar o Editar) -->
                        <h2 class="text-center mb-4">{{ isEdit ? 'Editar Usuario' : 'Registrar Usuario' }}</h2>
                        
                        <!-- Formulario para registrar o editar un usuario -->
                        <form class="user" @submit.prevent="registerEdit">
                            <!-- Campo para ingresar el nombre completo -->
                            <div class="form-group">
                                <input type="text" v-model="fullName" id="fullName" class="form-control form-control-user"
                                    placeholder="Nombre completo" required />
                            </div>
                            <!-- Campo para ingresar el correo electrónico -->
                            <div class="form-group">
                                <input type="email" v-model="email" id="email" class="form-control form-control-user"
                                    placeholder="Correo electrónico" required />
                            </div>
                            <!-- Campo para el rol solo si está en modo edición (no se puede cambiar el rol) -->
                            <div v-if="isEdit">
                                <div class="form-group">
                                    <input type="text" v-model="userRole" id="userRole" class="form-control form-control-user"
                                        placeholder="Cliente" :readonly="isEdit" />
                                </div>
                            </div>
                            <!-- Campos para la contraseña y confirmación, solo en modo de registro (cuando no es edición) -->
                            <div v-if="!isEdit">
                                <div class="form-group">
                                    <input type="password" v-model="password" id="password" class="form-control form-control-user"
                                        placeholder="Contraseña" required />
                                </div>
                                <div class="form-group">
                                    <input type="password" v-model="confirmPassword" id="confirmPassword"
                                        class="form-control form-control-user" placeholder="Confirmar contraseña" required />
                                </div>
                            </div>
                            <!-- Botón dinámico según la acción (Registrar o Actualizar) -->
                            <button type="submit" class="btn btn-primary btn-block">
                                {{ isEdit ? 'Actualizar' : 'Registrar' }}
                            </button>
                        </form>

                        <!-- Mostrar mensaje de error en caso de fallo -->
                        <div v-if="error" class="mt-3 alert alert-danger">
                            {{ error }}
                        </div>

                        <!-- Mostrar mensaje de éxito cuando la operación es exitosa -->
                        <div v-if="successMessage" class="mt-3 alert alert-success">
                            {{ successMessage }}
                        </div>

                        <!-- Enlace para iniciar sesión, solo se muestra en el modo de registro -->
                        <div v-if="!isEdit" class="text-center mt-3">
                            <router-link to="/">¿Ya tienes una cuenta? Inicia sesión</router-link>
                        </div>

                        <!-- Enlace para volver al panel de control, solo se muestra en el modo de edición -->
                        <div v-if="isEdit" class="text-center mt-3">
                            <router-link to="/dashboard">Volver al panel de control</router-link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue'; // Importamos funciones reactivas y el hook para montar el componente
import { useRoute } from 'vue-router'; // Para acceder a las rutas y obtener información de ellas
import { updateUser } from '@/services/userService'; // Servicio para actualizar un usuario
import { register } from '@/services/authService'; // Servicio para registrar un nuevo usuario

export default {
    setup() {
        const route = useRoute(); // Obtenemos información sobre la ruta actual

        // Definimos variables reactivas
        const fullName = ref(''); // Nombre completo del usuario
        const email = ref(''); // Correo electrónico del usuario
        const userRole = ref('Cliente'); // Rol del usuario, por defecto es "Cliente"
        const password = ref(''); // Contraseña (solo en modo registro)
        const confirmPassword = ref(''); // Confirmación de la contraseña
        const error = ref(null); // Variable para almacenar los mensajes de error
        const successMessage = ref(null); // Variable para almacenar los mensajes de éxito

        const isEdit = ref(false); // Determina si estamos en modo edición o registro
        const userId = ref(null); // Almacena el ID del usuario en modo edición

        // Función que maneja el registro o edición del usuario
        const registerEdit = async () => {
            // Limpiamos mensajes de error y éxito previos
            error.value = null;
            successMessage.value = null;

            try {
                if (isEdit.value) {
                    // Si estamos en modo edición, actualizamos el usuario
                    const updatedUser = await updateUser(userId.value, fullName.value, email.value, userRole.value);
                    // Capturamos el mensaje de éxito que proviene del servidor
                    successMessage.value = updatedUser.data.message || 'Usuario actualizado exitosamente!';
                    
                    // Actualizamos la información del usuario en localStorage
                    const userInStorage = JSON.parse(localStorage.getItem('user')); // Obtenemos el usuario del almacenamiento local
                    // Actualizamos los datos del usuario
                    userInStorage.full_name = fullName.value;
                    userInStorage.mail = email.value;
                    userInStorage.user_role = userRole.value;
                    localStorage.setItem('user', JSON.stringify(userInStorage)); // Guardamos los cambios en localStorage
                } else {
                    // Si estamos en modo registro, verificamos que las contraseñas coincidan
                    if (password.value !== confirmPassword.value) {
                        error.value = 'Las contraseñas no coinciden';
                        return; // Salimos de la función si las contraseñas no coinciden
                    }
                    // Registramos un nuevo usuario
                    const response = await register(fullName.value, email.value, userRole.value, password.value);
                    // Capturamos el mensaje de éxito que proviene del servidor
                    successMessage.value = response.data.message || 'Usuario registrado exitosamente!';
                }
            } catch (err) {
                // Capturamos errores específicos de la API y mostramos el mensaje de error que proviene del servidor
                error.value = err.response?.data?.detail || 'Error al procesar la solicitud';
                console.error(err); // Mostramos el error en la consola
            }
        };

        // Cuando el componente se monta, verificamos si estamos en modo edición
        onMounted(() => {
            if (route.name === 'EditProfile') {
                isEdit.value = true; // Modo edición activado
                const user = JSON.parse(localStorage.getItem('user')); // Obtenemos el usuario del almacenamiento local
                userId.value = user.user_id; // Asignamos el ID del usuario

                // Cargamos los datos del usuario para mostrarlos en el formulario
                fullName.value = user.full_name;
                email.value = user.mail;
                userRole.value = user.user_role;
            }
        });

        // Retornamos las variables y funciones para que puedan ser utilizadas en el template
        return {
            fullName,
            email,
            userRole,
            password,
            confirmPassword,
            error,
            successMessage,
            isEdit,
            registerEdit
        };
    }
};
</script>

<style>
/* Puedes agregar estilos personalizados aquí */
</style>
