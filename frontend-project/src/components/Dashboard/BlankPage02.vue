<template>
    <!-- Begin Page Content -->
    <div class="container-fluid">
        <!-- Page Heading -->
        <h1 class="h3 mb-4 text-gray-800">Blank Page 02</h1>
        
        <!-- Componente hijo que emite la categoría seleccionada -->
        <CategorySelect @category-selected="handleCategorySelected" />

        <!-- Mostramos la categoría seleccionada en el padre -->
        <p>Categoría seleccionada: {{ selectedCategory }}</p>
    </div>
    <!-- /.container-fluid -->
</template>

<script>
import { ref } from 'vue'; // Importamos ref de Vue para crear variables reactivas
import CategorySelect from '../Category/CategorySelect.vue'; // Importamos el componente hijo

export default {
    name: 'BlankPage02',
    
    components: {
        CategorySelect, // Registramos el componente hijo
    },
    
    setup() {
        // Definimos una referencia reactiva para la categoría seleccionada
        const selectedCategory = ref(null);

        // Método para manejar el evento emitido por el componente hijo
        const handleCategorySelected = (categoryId) => {
            selectedCategory.value = categoryId; // Actualizamos la categoría seleccionada
            console.log(selectedCategory.value);
        };

        // Retornamos las referencias y métodos al template
        return {
            selectedCategory,
            handleCategorySelected,
        };
    },
};
</script>

<style scoped>
/* Si necesitas añadir estilos personalizados, puedes hacerlo aquí */
</style>
