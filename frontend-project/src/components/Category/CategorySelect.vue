<template>
    <div class="form-group">
      <label for="categorySelect">Seleccione una categoría</label>
        <!-- Input para buscar la categoría -->
        <input 
            type="text" 
            class="form-control" 
            placeholder="Buscar categoría..." 
            v-model="searchQuery" 
            @input="searchCategoryByName" 
            aria-label="Buscar categoría"
        />
      
        <!-- Select que muestra los resultados -->
        <select 
            class="form-control mt-2" 
            id="categorySelect" 
            v-model="selectedCategory">
            <option v-for="category in categories" :key="category.category_id" :value="category.category_id">
            {{ category.category_name }}
            </option>
            <option v-if="categories.length === 0" disabled>No se encontraron categorías</option>
        </select>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import { getAllActiveCategories, getCategoryByName } from '@/services/categoryService';
  
  export default {
    name: 'CategorySelect',
    setup() {
      const categories = ref([]); // Almacena las categorías
      const selectedCategory = ref(''); // Categoría seleccionada
      const searchQuery = ref(''); // Query de búsqueda
  
      // Función para obtener todas las categorías activas al cargar el componente
      const fetchAllCategories = async () => {
        try {
          const response = await getAllActiveCategories();
          categories.value = response.data; // Asigna las categorías activas
        } catch (error) {
          console.error('Error obteniendo categorías activas:', error);
        }
      };
  
      // Función para buscar categorías por nombre al escribir
      const searchCategoryByName = async () => {
        if (searchQuery.value.trim() === '') {
          // Si el input está vacío, muestra todas las categorías
          await fetchAllCategories();
        } else {
          try {
            const response = await getCategoryByName(searchQuery.value);
            categories.value = response.data.length > 0 ? response.data : []; // Asigna los resultados al select
          } catch (error) {
            console.error('Error buscando categoría por nombre:', error);
            categories.value = []; // Limpia la lista si no hay resultados
          }
        }
      };
  
      // Llama a la función para obtener todas las categorías activas al montar el componente
      onMounted(() => {
        fetchAllCategories();
      });
  
      return {
        categories,
        selectedCategory,
        searchQuery,
        searchCategoryByName,
      };
    }
  };
  </script>
  
  <style scoped>
 
  </style>