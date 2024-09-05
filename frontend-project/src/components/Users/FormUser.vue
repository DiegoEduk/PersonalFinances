<template>
    <div>
      <!-- El formulario para editar usuario se carga aquí -->
      <form class="user" @submit.prevent="saveChanges">
        <div class="form-group">
          <label for="fullName">Nombre Completo</label>
          <input type="text" v-model="localUser.fullName" id="fullName" class="form-control form-control-user" placeholder="Nombre completo" required />
        </div>
        <div class="form-group">
          <label for="email">Correo Electrónico</label>
          <input type="email" v-model="localUser.email" id="email" class="form-control form-control-user" placeholder="Correo electrónico" required />
        </div>
        <div class="form-group" v-if="canEditRole">
          <label for="userRole">Rol del Usuario</label>
          <input type="text" v-model="localUser.userRole" id="userRole" class="form-control form-control-user" placeholder="Rol del usuario" required />
        </div>
        <b-button type="submit" variant="primary">Guardar</b-button>
        <b-button @click="$emit('close')" variant="secondary">Cerrar</b-button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      user: {
        type: Object,
        default: () => ({})
      },
      canEditRole: {
        type: Boolean,
        default: false
      }
    },
    data() {
      return {
        localUser: { ...this.user } // Clonar los datos del usuario recibido
      };
    },
    methods: {
      saveChanges() {
        this.$emit('update'); // Emitir evento para actualizar el usuario
      }
    }
  };
  </script>
  
  <style scoped>
  /* Agrega estilos según sea necesario */
  </style>
  