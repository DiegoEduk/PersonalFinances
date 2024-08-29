<template>
    <div>
        <form @submit.prevent="getToken">
            <div>
                <label for="username">Username:</label>
                <input type="text" id="username" v-model="username" required />
            </div>
            <div>
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" required />
            </div>
            <button type="submit">Obtener Token</button>
        </form>
        <p v-if="token">Token: {{ token }}</p>
        <p v-if="error">{{ error }}</p>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            username: '',
            password: '',
            token: null,
            error: null,
        };
    },
    methods: {
        async getToken() {
            try {
                const response = await axios.post(
                    'https://personalfinances-5czq.onrender.com/access/token',
                    new URLSearchParams({
                        grant_type: '',
                        username: this.username,
                        password: this.password,
                        scope: '',
                        client_id: '',
                        client_secret: '',
                    }),
                    {
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'Accept': 'application/json',
                        },
                    }
                );

                // Si la solicitud es exitosa, almacena el token en el estado
                this.token = response.data.access_token;
                this.error = null; // Limpiar el error si la solicitud es exitosa
            } catch (error) {
                // Si hay un error, almacena el mensaje de error en el estado
                this.token = null; // Limpiar el token en caso de error
                this.error = 'Error: ' + (error.response?.data?.detail || error.message);
            }
        },
    },
};
</script>
