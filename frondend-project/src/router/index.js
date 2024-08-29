import { createRouter, createWebHistory } from 'vue-router';
import LoginView from '../views/LoginView.vue';
import ForgotPassView from '../views/ForgotPassView.vue';
import NotFoundView from '../views/NotFoundView.vue';

const routes = [
  // Ruta por defecto que apunta a LoginView
  { path: '/', name: 'Login', component: LoginView },
  // Otras rutas
  { path: '/forgot-password', name: 'ForgotPass', component: ForgotPassView },
  { path: '/not-found', name: 'NotFound', component: NotFoundView },
  // Redirección en caso de ruta no encontrada
  { path: '/:pathMatch(.*)*', redirect: '/not-found' },
];

const router = createRouter({
  history: createWebHistory(process.env.VITE_API_URL),
  routes,
});

export default router;
