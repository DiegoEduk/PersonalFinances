<!-- DynamicComponent.vue -->
<template>
  <!-- La directiva <component :is="currentComponent"> en Vue 3 permite renderizar dinámicamente componentes basados en el valor de currentComponent -->
  <component :is="currentComponent"></component>
</template>

<script>
export default {
  props: {
    currentComponent: {
      type: [String, Object], // Acepta tanto nombres de componentes como objetos de componente
      required: true
    }
  }
};
</script>
