<template>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card shadow-lg my-5">
                    <div class="card-body">
                        <h2 class="text-center">Registrar Usuario</h2>
                        <form class="user" @submit.prevent="registerUser">
                            <div class="form-group">
                                <label for="fullName">Nombre Completo</label>
                                <input type="text" v-model="fullName" id="fullName" class="form-control form-control-user"
                                    placeholder="Nombre completo" required />
                            </div>
                            <div class="form-group">
                                <label for="email">Correo Electrónico</label>
                                <input type="email" v-model="email" id="email" class="form-control form-control-user"
                                    placeholder="Correo electrónico" required />
                            </div>
                            <div class="form-group">
                                <label for="userRole">Rol del Usuario</label>
                                <input type="text" v-model="userRole" id="userRole" class="form-control form-control-user"
                                    placeholder="Cliente" value="Cliente" readonly />
                            </div>
                            <div class="form-group">
                                <label for="password">Contraseña</label>
                                <input type="password" v-model="password" id="password" class="form-control form-control-user"
                                    placeholder="Contraseña" required />
                            </div>
                            <div class="form-group">
                                <label for="confirmPassword">Confirmar Contraseña</label>
                                <input type="password" v-model="confirmPassword" id="confirmPassword"
                                    class="form-control form-control-user" placeholder="Confirmar contraseña" required />
                            </div>
                            <button type="submit" class="btn btn-primary btn-block">Registrar</button>
                        </form>
                        <div v-if="error" class="mt-3 alert alert-danger">
                            {{ error }}
                        </div>
                        <div v-if="successMessage" class="mt-3 alert alert-success">
                            {{ successMessage }}
                        </div>
                        <div class="text-center mt-3">
                            <router-link to="/">Ya tienes una cuenta? Inicia sesión</router-link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { register } from '@/services/authService'; // Asegúrate de que este servicio esté definido

export default {
    setup() {
        const router = useRouter();
        const fullName = ref('');
        const email = ref('');
        const userRole = ref('');
        const password = ref('');
        const confirmPassword = ref('');
        const error = ref(null);
        const successMessage = ref(null);

        const registerUser = async () => {
            error.value = null; // Limpiar posibles mensajes de error
            successMessage.value = null; // Limpiar posibles mensajes de éxito
            
            if (password.value !== confirmPassword.value) {
                error.value = 'Las contraseñas no coinciden';
                return;
            }

            try {
                await register(fullName.value, email.value, userRole.value, password.value);
                successMessage.value = 'Usuario registrado exitosamente!';
            } catch (err) {
                error.value = 'Error al registrar el usuario';
                console.error(err);
            }
        };

        return {
            fullName,
            email,
            userRole,
            password,
            confirmPassword,
            error,
            successMessage,
            registerUser
        };
    }
};
</script>

<style>
/* Agrega estilos según sea necesario */
</style>