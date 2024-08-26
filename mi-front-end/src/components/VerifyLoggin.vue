<template>
    <div>
        <button @click="toggleLogin">{{ isLoggedIn ? 'Cerrar Sesión' : 'Iniciar Sesión' }}</button>
        <p v-if="isLoggedIn">Has iniciado sesión</p>
        <p v-else>No has iniciado sesión</p>
    </div>
</template>

<script>
export default {
    data() {
        return {
            isLoggedIn: false
        };
    },
    methods: {
        toggleLogin(){
            this.isLoggedIn = !this.isLoggedIn;
        }
    }
};
</script>