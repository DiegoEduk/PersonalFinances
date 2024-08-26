<template>
    <img id="logoSena" :src="imagenUrl" :alt="imagenAlt">
</template>

<script>
export default {
    data() {
        return {
            imagenUrl: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRTlt8LLMIhvxI5Z4xhmrGw1AknxbRYaJ_43A&s",
            imagenAlt: "Logo del SENA"
        };
    }
};
</script>

<style scoped>
#logoSena {
  border-radius: 50%;
  border: 5px solid gray;
  padding: 1em;
  margin: 1em;
}
</style>