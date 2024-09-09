
<template>
  <SpinnerGlobal />
  <router-view />
</template>

<script>
import SpinnerGlobal from "./components/UI/SpinnerGlobal.vue";

export default {
  components: {
    SpinnerGlobal, // Incluir el spinner global
  },
};
</script>