<template>
    <div>
        <input v-model="mensaje" placeholder="Escribe un mensaje">
        <p>Mensaje: {{ mensaje }}</p>
    </div>
</template>

<script>
export default {
    data() {
        return {
            mensaje: ''
        };
    }
};
</script>