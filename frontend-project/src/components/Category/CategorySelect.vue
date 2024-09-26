<template>
  <div class="form-container" @click="toggleDropdown">
    <!-- <label for="categorySelect">Seleccione una categoría</label> -->

    <!-- Contenedor que actúa como select -->
    <div class="custom-select">
      <div class="selected-option">{{ selectedCategoryName || 'Seleccione una categoría' }}</div>

      <!-- Dropdown que contiene el input y las opciones -->
      <div v-if="dropdownOpen" class="dropdown-options" @click.stop>
        <!-- Input para buscar la categoría -->
        <input 
          type="text" 
          class="search-input" 
          placeholder="Buscar ..." 
          v-model="searchQuery" 
          @input="filterCategories"
        />

        <!-- Opciones de categorías -->
        <div 
          v-for="category in filteredCategories" 
          :key="category.category_id" 
          class="option" 
          @click.stop="selectCategory(category)"
        >
          {{ category.category_name }}
        </div>

        <!-- Mensaje cuando no hay categorías -->
        <div v-if="filteredCategories.length === 0" class="no-options">
          No se encontraron categorías
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue';
import { getAllActiveCategories } from '@/services/categoryService';

export default {
  name: 'CategorySelect',
  props: {
    selectedCategoryId: {
      type: Number,
      default: null
    }
  },
  setup(props, { emit }) {
    const categories = ref([]); // Almacena las categorías
    const selectedCategory = ref(props.selectedCategoryId); // Inicializa con la categoría seleccionada
    const searchQuery = ref(''); // Query de búsqueda
    const dropdownOpen = ref(false); // Estado del dropdown
    const filteredCategories = ref([]); // Categorías filtradas

    // Función para obtener todas las categorías activas al cargar el componente
    const fetchAllCategories = async () => {
      try {
        const response = await getAllActiveCategories();
        categories.value = response.data;
        filteredCategories.value = response.data; // Inicialmente todas las categorías
      } catch (error) {
        console.error('Error obteniendo categorías activas:', error);
      }
    };

    // Filtra las categorías según la búsqueda
    const filterCategories = () => {
      const query = searchQuery.value.toLowerCase();
      filteredCategories.value = categories.value.filter(category =>
        category.category_name.toLowerCase().includes(query)
      );
    };

    // Función para seleccionar una categoría
    const selectCategory = (category) => {
      selectedCategory.value = category.category_id;
      dropdownOpen.value = false; // Cierra el dropdown
      // Emitimos el evento `category-selected` al padre, pasando la categoría seleccionada
      emit('category-selected', category.category_id);
    };

    // Función para alternar el dropdown
    const toggleDropdown = () => {
      dropdownOpen.value = !dropdownOpen.value;
    };

    // Cerrar el dropdown al hacer clic fuera del componente
    const closeDropdownOnClickOutside = (event) => {
      if (!event.target.closest('.form-container')) {
        dropdownOpen.value = false;
      }
    };

    // Añadir el event listener al montar el componente
    onMounted(() => {
      fetchAllCategories();
      document.addEventListener('click', closeDropdownOnClickOutside);
    });

    // Quitar el event listener al desmontar el componente
    onBeforeUnmount(() => {
      document.removeEventListener('click', closeDropdownOnClickOutside);
    });

    // Sincronizar `selectedCategory` con `selectedCategoryId` prop cuando cambie
    watch(() => props.selectedCategoryId, (newVal) => {
      selectedCategory.value = newVal;
    });

    // Devuelve el nombre de la categoría seleccionada
    const selectedCategoryName = computed(() => {
      const category = categories.value.find(cat => cat.category_id === selectedCategory.value);
      return category ? category.category_name : null;
    });

    return {
      categories,
      selectedCategory,
      searchQuery,
      dropdownOpen,
      filteredCategories,
      selectedCategoryName,
      filterCategories,
      selectCategory,
      toggleDropdown,
    };
  }
};
</script>

<style scoped>
.form-container {
  display: flex;
  flex-direction: column;
  max-width: 100%;
  margin: 0 auto;
}

label {
  margin-bottom: 8px;
}

/* Custom select styles */
.custom-select {
  position: relative;
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 8px;
  cursor: pointer;
}

.selected-option {
  font-size: 16px;
}

.dropdown-options {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 4px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 2;
}

.search-input {
  padding: 8px;
  width: calc(100% - 16px); /* Restar padding total */
  font-size: 16px;
  border: none;
  border-bottom: 1px solid #ccc;
}

.option {
  padding: 8px;
  font-size: 16px;
  cursor: pointer;
}

.option:hover {
  background-color: #f1f1f1;
}

.no-options {
  padding: 8px;
  font-size: 14px;
  color: #999;
}
</style>
