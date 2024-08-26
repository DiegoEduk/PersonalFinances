<template>
    <div>
        <p>Contador: {{ contador }}</p>
        <button @click="incrementar">Incrementar</button>
    </div>
</template>

<script>
import { ref } from 'vue';

export default {
    setup() {
        // Definimos una propiedad reactiva usando ref
        const contador = ref(0);
        // Método para incrementar el contador
        const incrementar = () => {
            // Modificamos el valor de la propiedad reactiva
            contador.value++;
        };
        return { contador, incrementar };
    }
}
</script>
