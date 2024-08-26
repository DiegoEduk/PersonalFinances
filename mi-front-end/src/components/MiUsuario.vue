<template>
  <div>
    <p>Nombre: {{ persona.nombre }}</p>
    <p>Edad: {{ persona.edad }}</p>
    <button @click="cumplirAnios">Cumplir Años</button>
  </div>
</template>

<script>
import { reactive } from 'vue';

export default {
  setup() {
    // Definimos un objeto reactivo usando reactive
    const persona = reactive({
      nombre: 'Juan',
      edad: 25
    });

    // Método para incrementar la edad
    const cumplirAnios = () => {
      persona.edad++;
    };

    return { persona, cumplirAnios };
  }
}
</script>