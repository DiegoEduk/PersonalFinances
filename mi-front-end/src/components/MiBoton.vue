<template>
    <button @click="enviarMensaje">Has click aquí</button>
</template>

<script>
export default {
    methods: {
        enviarMensaje(){
            this.$emit ('mensaje-enviado', "Hola desde componente Hijo");
        }
    }
};
</script>