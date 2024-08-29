import { createApp } from 'vue'
import App from './App.vue'
import router from './router'; // Asegúrate de que el router esté importado correctamente
import '../public/css/sb-admin-2.min.css';

const app = createApp(App);

app.use(router); // Asegúrate de que esté registrado con la aplicación
app.mount('#app');