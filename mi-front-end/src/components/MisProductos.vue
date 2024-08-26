<template>
    <ul>
        <li v-for="(producto, index) in productos" :key="index">{{ producto.nombre }} - ${{ producto.precio + 4}}</li>
    </ul>
</template>

<script>
export default {
    data() {
        return {
            productos: [
                { nombre: 'Camiseta', precio: 20 },
                { nombre: 'Pantalones', precio: 40 },
                { nombre: 'Zapatos', precio: 60 }
            ]
        };
    }
};
</script>