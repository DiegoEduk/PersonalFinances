import { createApp } from 'vue'
import App from './App.vue'
import router from './router'; // Asegúrate de que el router esté importado correctamente
import '../public/css/sb-admin-2.min.css';
import { createPinia } from 'pinia';

const app = createApp(App);

// Crear la instancia de Pinia
const pinia = createPinia();

// Usar Pinia en la aplicación
app.use(pinia);
app.use(router); // Asegúrate de que esté registrado con la aplicación
app.mount('#app');