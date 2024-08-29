import axios from 'axios';
import { useAuthStore } from '@/store'; // Importa el store de Pinia

// Crear una instancia de Axios
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL, // Usar la URL de la API desde el archivo .env
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  }
});

// Interceptor para añadir el token de autorización
api.interceptors.request.use(config => {
    const authStore = useAuthStore(); // Obtener el store de autenticación
    const token = authStore.accessToken;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`; // Añadir el token a las cabeceras
    }
    return config;
  }, error => {
    return Promise.reject(error);
  });


// Interceptor para manejar errores
api.interceptors.response.use(response => {
    return response;
  }, error => {
    if (error.response && error.response.status === 401 && error.response.data.detail === "Invalid token") {
        // Redirigir a la página de login
        router.push('/'); // Asegúrate de que el router esté correctamente configurado
    }
    return Promise.reject(error);
});

export default api;