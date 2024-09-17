<template>
  <!-- Capa que cubre toda la pantalla cuando loading está activo -->
  <div v-if="loading" class="spinner-overlay">
    <div class="spinner-container">
      <div class="spinner-border spinner" role="status">
        <span class="sr-only">Loading...</span>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'; // Importa computed
import { useSpinnerStore } from "@/store/spinner";

export default {
  setup() {
    // Obtenemos el store del spinner
    const spinnerStore = useSpinnerStore();
    return {
      loading: computed(() => spinnerStore.loading),
    };
  },
};
</script>

<style scoped>
/* Capa que cubre toda la pantalla */
.spinner-overlay {
  position: fixed;
  top: 0;
  left: 0;
  font-size: 2em;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5); /* Fondo negro con transparencia */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999; /* Asegura que esté sobre todos los elementos */
}

/* Centrar el spinner */
.spinner-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* mas grande y colorido */
.spinner{
  width: 4rem;
  height: 4rem;
  color: white;
}
</style>
