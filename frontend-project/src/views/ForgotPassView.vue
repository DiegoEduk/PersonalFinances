<template>
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-xl-10 col-lg-12 col-md-9">
          <div class="card o-hidden border-0 shadow-lg my-5">
            <div class="card-body p-0">
              <div class="row">
                <div class="col-lg-6 d-none d-lg-block bg-password-image"></div>
                <div class="col-lg-6">
                  <div class="p-5">
                    <div class="text-center">
                      <h1 class="h4 text-gray-900 mb-2">¿ Recordar contraseña ?</h1>
                      <p class="mb-4">Simplemente ingrese su dirección de correo electrónico a continuación y le enviaremos un código para restablecer su contraseña.</p>
                    </div>
  
                    <!-- Fase 1: Ingreso de email para enviar código de reseteo -->
                    <div v-if="!showPasswordForm">
                      <form @submit.prevent="sendResetCode" class="user">
                        <div class="form-group">
                          <input 
                            type="email" 
                            class="form-control form-control-user" 
                            v-model="email" 
                            placeholder="Ingrese su correo electrónico" 
                            required 
                          />
                        </div>
                        <button type="submit" class="btn btn-primary btn-user btn-block">
                          Enviar código
                        </button>
                      </form>
                    </div>
  
                    <!-- Fase 2: Introducción de código, nueva contraseña y confirmación -->
                    <div v-if="showPasswordForm">
                      <form @submit.prevent="resetPassword" class="user">
                        <div class="form-group">
                          <input 
                            type="password" 
                            class="form-control form-control-user" 
                            v-model="newPassword" 
                            placeholder="Nueva contraseña" 
                            required 
                          />
                        </div>
                        <div class="form-group">
                          <input 
                            type="password" 
                            class="form-control form-control-user" 
                            v-model="confirmPassword" 
                            placeholder="Confirmar contraseña" 
                            required 
                          />
                        </div>
                        <div class="form-group">
                          <input 
                            type="text" 
                            class="form-control form-control-user" 
                            v-model="code" 
                            placeholder="Ingrese el código enviado a su correo" 
                            required 
                          />
                        </div>
                        <button type="submit" class="btn btn-primary btn-user btn-block">
                          Actualizar contraseña
                        </button>
                      </form>
                    </div>
  
                    <!-- Mostrar errores -->
                    <div v-if="error" class="alert alert-danger mt-3">
                      {{ error }}
                    </div>
  
                    <hr>
                    <div class="text-center">
                      <router-link class="small" to="/">Ya tienes una cuenta? Iniciar sesión</router-link>
                    </div>
                    <div class="text-center">
                      <router-link class="small" to="/register">¿No tienes una cuenta? ¡Regístrate!</router-link>
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
  import { requestResetCode, changePassword } from "@/services/authService"; // Importa tus servicios de API
  
  export default {
    data() {
      return {
        email: "",
        newPassword: "",
        confirmPassword: "",
        code: "",
        error: null,
        showPasswordForm: false,
      };
    },
    methods: {
      // Enviar código de reseteo al correo
      async sendResetCode() {
        this.error = null; // Limpiar error previo
        try {
          await requestResetCode(this.email);
          this.showPasswordForm = true; // Mostrar los inputs adicionales
        } catch (err) {
          this.error = err.response?.data?.detail || "Error enviando el código. Intente de nuevo.";
        }
      },
  
      // Verificar código y actualizar contraseña
      async resetPassword() {
        this.error = null; // Limpiar error previo
  
        // Validar que las contraseñas coincidan
        if (this.newPassword !== this.confirmPassword) {
          this.error = "Las contraseñas no coinciden.";
          return;
        }
  
        try {
          await changePassword(this.email, this.newPassword, this.code);
          alert("¡Contraseña actualizada con éxito!");
          this.$router.push("/login"); // Redirigir a la página de login
        } catch (err) {
          this.error = err.response?.data?.detail || "Error actualizando la contraseña. Verifique el código.";
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Puedes agregar estilos personalizados aquí */
  </style>
  