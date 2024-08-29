// src/store/index.js
import { defineStore } from 'pinia';
import { login } from '@/services/authService'; // Importa el servicio de autenticación

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    permissions: [],
    accessToken: null,
    authError: null,
  }),
  actions: {
    async login(username, password) {
      try {
        const response = await login(username, password); // Usa el servicio para la autenticación
        
        this.user = response.data.user;
        this.permissions = response.data.permissions;
        this.accessToken = response.data.access_token;
        this.authError = null;

        localStorage.setItem('access_token', this.accessToken);
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.authError = error.response.data.detail;
        } else {
          this.authError = 'Ocurrió un error inesperado';
        }
      }
    },

    logout() {
      this.user = null;
      this.permissions = [];
      this.accessToken = null;
      this.authError = null;
      localStorage.removeItem('access_token');
    }
  }
});
