<template>
    <!-- Contenedor principal del contenido de la página -->
    <div class="container-fluid">
      
      <!-- Título de la página -->
      <h1 class="h3 mb-2 text-gray-800">Usuarios</h1>
  
      <!-- Tarjeta que contiene la tabla de usuarios -->
      <div class="card shadow mb-4">
        
        <!-- Encabezado de la tarjeta -->
        <div class="card-header py-3">
          <h6 class="m-0 font-weight-bold text-primary">Lista de Usuarios</h6>
        </div>
        
        <!-- Cuerpo de la tarjeta -->
        <div class="card-body">
          <div class="table-responsive">
            <!-- Tabla para mostrar la lista de usuarios -->
            <table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
              <thead>
                <tr>
                  <th>Nombre</th>
                  <th>Correo</th>
                  <th>Rol</th>
                  <th>Estado</th>
                  <th>Última Actualización</th>
                </tr>
              </thead>
              <tbody>
                <!-- Itera sobre el arreglo de usuarios y crea una fila por cada usuario -->
                <tr v-for="user in users" :key="user.user_id">
                  <td>{{ user.full_name }}</td>
                  <td>{{ user.mail }}</td>
                  <td>{{ user.user_role }}</td>
                  <td>{{ user.user_status ? 'Activo' : 'Inactivo' }}</td>
                  <td>{{ formatDate(user.updated_at) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <!-- Controles de paginación -->
          <div class="pagination-controls">
            <button class="btn btn-primary m-3" @click="prevPage" :disabled="currentPage === 1">Anterior</button>
            <span>Página {{ currentPage }} de {{ totalPages }}</span>
            <button class="btn btn-primary m-3" @click="nextPage" :disabled="currentPage === totalPages">Siguiente</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  // Importa la función para obtener usuarios paginados desde el servicio API
  import { getUsersByPage } from '@/services/userService'; // Asegúrate de ajustar la ruta según la estructura de tu proyecto
  
  export default {
    data() {
      return {
        users: [],         // Arreglo para almacenar la lista de usuarios obtenidos
        currentPage: 1,    // Página actual de la paginación
        totalPages: 0,     // Total de páginas disponibles
      };
    },
    methods: {
      /**
       * Método para obtener los usuarios de la página actual
       */
      async fetchUsers() {
        try {
          // Llama a la función getUsersByPage pasando la página actual
          const response = await getUsersByPage(this.currentPage);
          
          // Asigna los usuarios obtenidos al arreglo users
          this.users = response.data.users;
          
          // Actualiza el número total de páginas según la respuesta del servidor
          this.totalPages = response.data.total_pages;
        } catch (error) {
          // Maneja errores de la petición
          alert('Error al obtener los usuarios:', error);
        }
      },
      
      /**
       * Método para avanzar a la siguiente página
       */
      nextPage() {
        if (this.currentPage < this.totalPages) {
          this.currentPage++;     // Incrementa el número de página
          this.fetchUsers();      // Obtiene los usuarios de la nueva página
        }
      },
      
      /**
       * Método para retroceder a la página anterior
       */
      prevPage() {
        if (this.currentPage > 1) {
          this.currentPage--;     // Decrementa el número de página
          this.fetchUsers();      // Obtiene los usuarios de la nueva página
        }
      },
      
      /**
       * Método para formatear las fechas al formato deseado
       * @param {String} dateString - La cadena de fecha a formatear
       * @returns {String} - Fecha formateada
       */
      formatDate(dateString) {
        const options = { 
          year: 'numeric', 
          month: 'numeric', 
          day: 'numeric', 
          hour: '2-digit', 
          minute: '2-digit' 
        };
        return new Date(dateString).toLocaleDateString('es-ES', options);
      },
    },
    /**
     * Hook del ciclo de vida que se ejecuta cuando el componente se monta
     */
    mounted() {
      this.fetchUsers(); // Llama al método para obtener los usuarios al cargar el componente
    },
  };
  </script>
  
  <style scoped>
  /* Estilos opcionales para mejorar la apariencia de los controles de paginación */
  
  </style>
  