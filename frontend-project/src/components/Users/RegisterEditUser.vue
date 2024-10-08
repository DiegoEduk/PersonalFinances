<template>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-xl-10 col-lg-12 col-md-9">
                <div class="card o-hidden border-0 shadow-lg my-5">
                    <div class="card-body p-0">
                        <div class="row">
                            <div class="col-lg-6 d-none d-lg-block bg-password-image">
                                <div class="m-5">
                                    <!-- Aquí cargar visualizar imagen -->
                                    <img v-if="imagePreview" :src="imagePreview" alt="Previsualización de imagen"
                                        class="img-fluid mt-3" />
                                </div>
                            </div>
                            <div class="col-lg-6">
                                <div class="m-5">
                                    <div class="card-body">
                                        <h2 class="text-center mb-4">{{ isEdit ? 'Editar Usuario' : 'Registrar Usuario' }}</h2>
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

                                            <!-- Campo para el rol solo si está en modo edición -->
                                            <div v-if="isEdit">
                                                <div class="form-group">
                                                    <input type="text" v-model="userRole" id="userRole"
                                                        class="form-control form-control-user" placeholder="Cliente" :readonly="isEdit" />
                                                </div>
                                            </div>

                                            <!-- Campos para la contraseña y confirmación solo en modo registro -->
                                            <div v-if="!isEdit">
                                                <div class="form-group">
                                                    <input type="password" v-model="password" id="password"
                                                        class="form-control form-control-user" placeholder="Contraseña" required />
                                                </div>
                                                <div class="form-group">
                                                    <input type="password" v-model="confirmPassword" id="confirmPassword"
                                                        class="form-control form-control-user" placeholder="Confirmar contraseña" required />
                                                </div>
                                            </div>

                                            <!-- Campo para cargar la imagen -->
                                            <div class="form-group">
                                                <label for="imageUpload"  class="form-label">Cargar Imagen:</label>
                                                <input type="file" id="imageUpload" class="form-control" @change="onImageChange" accept="image/*" />
                                            </div>

                                            <!-- Botón dinámico según la acción (Registrar o Actualizar) -->
                                            <button type="submit" class="btn btn-primary btn-block">
                                                {{ isEdit ? 'Actualizar' : 'Registrar' }}
                                            </button>
                                        </form>

                                        <!-- Mostrar mensaje de error en caso de fallo -->
                                        <div v-if="error" class="mt-3 alert alert-danger">{{ error }}</div>

                                        <!-- Mostrar mensaje de éxito cuando la operación es exitosa -->
                                        <div v-if="successMessage" class="mt-3 alert alert-success">{{ successMessage }}</div>

                                        <!-- Enlace para iniciar sesión en modo registro -->
                                        <div v-if="!isEdit" class="text-center mt-3">
                                            <router-link to="/">¿Ya tienes una cuenta? Inicia sesión</router-link>
                                        </div>

                                        <!-- Enlace para volver al panel de control en modo edición -->
                                        <div v-if="isEdit" class="text-center mt-3">
                                            <router-link to="/dashboard">Volver al panel de control</router-link>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue'; 
import { useRoute } from 'vue-router'; 
import { updateUser } from '@/services/userService'; 
import { register } from '@/services/authService'; 

export default {
    setup() {
        const route = useRoute();
        const fullName = ref(''); 
        const email = ref(''); 
        const userRole = ref('Cliente'); 
        const password = ref(''); 
        const confirmPassword = ref(''); 
        const error = ref(null); 
        const successMessage = ref(null); 

        const isEdit = ref(false);
        const userId = ref(null); 
        const imageFile = ref(null); 
        const imagePreview = ref(null); 

        const registerEdit = async () => {
            error.value = null;
            successMessage.value = null;

            try {
                if (isEdit.value) {
                    const updatedUser = await updateUser(userId.value, fullName.value, email.value, userRole.value);
                    successMessage.value = updatedUser.data.message || 'Usuario actualizado exitosamente!';

                    const userInStorage = JSON.parse(localStorage.getItem('user')); 
                    userInStorage.full_name = fullName.value;
                    userInStorage.mail = email.value;
                    userInStorage.user_role = userRole.value;
                    localStorage.setItem('user', JSON.stringify(userInStorage)); 
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
                error.value = err.response?.data?.detail || 'Error al procesar la solicitud';
                console.error(err);
            }
        };

        const onImageChange = (event) => {
            const file = event.target.files[0];
            if (file) {
                imageFile.value = file;
                imagePreview.value = URL.createObjectURL(file);
            }
        };

        onMounted(() => {
            if (route.name === 'EditProfile') {
                isEdit.value = true;
                const user = JSON.parse(localStorage.getItem('user')); 
                userId.value = user.user_id;

                fullName.value = user.full_name;
                email.value = user.mail;
                userRole.value = user.user_role;
            }
        });

        return {
            fullName,
            email,
            userRole,
            password,
            confirmPassword,
            error,
            successMessage,
            isEdit,
            registerEdit,
            onImageChange,
            imagePreview
        };
    }
};
</script>

<style>
/* Puedes agregar estilos personalizados aquí */
.img-fluid {
    margin: 0px auto;
}
</style>
