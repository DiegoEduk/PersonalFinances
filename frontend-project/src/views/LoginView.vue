<template>
    <div class="container">
        <!-- Outer Row -->
        <div class="row justify-content-center">
            <div class="col-xl-10 col-lg-12 col-md-9">
                <div class="card o-hidden border-0 shadow-lg my-5">
                    <div class="card-body p-0">
                        <!-- Nested Row within Card Body -->
                        <div class="row">
                            <div class="col-lg-6 d-none d-lg-block bg-login-image align-self-center">
                                <div class="p-5">
                                    <img class="img-fluid" src="@/assets/img/logo.jpg" alt="Logo de la empresa">
                                </div>
                            </div>
                            <div class="col-lg-6">
                                <div class="p-5">
                                    <div class="text-center">
                                        <h1 class="h4 text-gray-900 mb-4">Bienvenido !</h1>
                                    </div>
                                    <!-- Mostrar error si existe -->
                                    <div v-if="errorMessage" class="alert alert-danger" role="alert">
                                        {{ errorMessage }}
                                    </div>
                                    <!-- Formulario de Login -->
                                    <form class="user" @submit.prevent="handleLogin">
                                        <!-- Campo de Email -->
                                        <div class="form-group">
                                            <input v-model="email" type="email" class="form-control form-control-user"
                                                id="exampleInputEmail" aria-describedby="emailHelp"
                                                placeholder="Enter Email Address...">
                                        </div>
                                        <!-- Campo de Contraseña -->
                                        <div class="form-group">
                                            <input v-model="password" type="password"
                                                class="form-control form-control-user" id="exampleInputPassword"
                                                placeholder="Password">
                                        </div>
                                        <!-- Checkbox para Recordar Contraseña -->
                                        <div class="form-group">
                                            <div class="custom-control custom-checkbox small">
                                                <input type="checkbox" class="custom-control-input" id="customCheck">
                                                <label class="custom-control-label" for="customCheck">Remember
                                                    Me</label>
                                            </div>
                                        </div>
                                        <!-- Botón de Login -->
                                        <button type="submit" class="btn btn-primary btn-user btn-block">
                                            Login
                                        </button>
                                        <hr>
                                        <a href="index.html" class="btn btn-google btn-user btn-block">
                                            <i class="fab fa-google fa-fw"></i> Login with Google
                                        </a>
                                        <a href="index.html" class="btn btn-facebook btn-user btn-block">
                                            <i class="fab fa-facebook-f fa-fw"></i> Login with Facebook
                                        </a>
                                    </form>
                                    <hr>
                                    <!-- Enlaces a otras páginas -->
                                    <div class="text-center">
                                        <router-link class="small" to="/forgot-password">Recordar Contraseña
                                            ?</router-link>
                                    </div>
                                    <div class="text-center">
                                        <router-link class="small" to="/register">Create an Account!</router-link>
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
import { ref } from 'vue';
import { useAuthStore } from '@/store'; // Importa el store de autenticación
import { useRouter } from 'vue-router'; // Importa Vue Router para la redirección

export default {
    setup() {
        // Obtén la instancia del store y el router
        const authStore = useAuthStore();
        const router = useRouter();

        // Define las propiedades reactivas para el email, la contraseña y el mensaje de error
        const email = ref('');
        const password = ref('');
        const errorMessage = ref(null); // Añade una propiedad para el mensaje de error

        // Método para manejar el login
        const handleLogin = async () => {
            try {
                await authStore.login(email.value, password.value); // Llama al método de login del store

                if (authStore.authError) {
                    // Si hay un error de autenticación, establece el mensaje de error
                    errorMessage.value = authStore.authError;
                } else {
                    // Redirige a la página de dashboard si el login es exitoso
                    router.push('/dashboard'); // Reemplaza '/dashboard' con la ruta que desees redirigir
                }
            } catch (error) {
                // Maneja errores inesperados
                errorMessage.value = 'Error durante el login: ' + error.message;
            }
        };

        // Retorna las propiedades y métodos que estarán disponibles en el template
        return {
            email,
            password,
            errorMessage, // Añade el mensaje de error al retorno
            handleLogin
        };
    }
};
</script>

<style scoped>
/* Estilos específicos para este componente pueden ir aquí */
</style>