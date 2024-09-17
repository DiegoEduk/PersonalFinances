<template>
    <!-- Begin Page Content -->
    <div class="container-fluid">

        <!-- Título de la página -->
        <h1 class="h3 mb-2 text-gray-800">Categorías</h1>

        <!-- Botón para registrar una nueva categoría -->
        <button @click="openCreateModal" class="btn btn-success mb-4">Registrar Categoría</button>

        <!-- DataTales Example -->
        <div class="card shadow mb-4">
            <div class="card-header py-3">
                <h6 class="m-0 font-weight-bold text-primary">Lista de Categorías</h6>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
                        <thead>
                            <tr>
                                <th>Nombre</th>
                                <th>Descripción</th>
                                <th>Estado</th>
                                <th></th>
                            </tr>
                        </thead>

                        <tbody>
                            <!-- Recorre la lista de categorías con v-for -->
                            <tr v-for="category in categories" :key="category.id">
                                <!-- Muestra los datos de cada categoría en cada td-->
                                <td>{{ category.category_name }}</td>
                                <td>{{ category.category_description }}</td>
                                <td>
                                    <div class="custom-control custom-switch">
                                        <input type="checkbox" class="custom-control-input" :id="`switch-${category.category_id}`" :checked="category.category_status" @change="toggleCategoryStatus(category)">
                                        <label class="custom-control-label" :for="`switch-${category.category_id}`">{{ category.category_status ? 'Activa' : 'Inactiva' }}</label>
                                    </div>
                                </td>
                                <!-- Botones para editar o eliminar una categoría  -->
                                <td>
                                    <button @click="openEditModal(category)" class="btn btn-outline-secondary"><i
                                            class="fa-solid fa-pen-to-square"></i></button>
                                    <button @click="deleteCategoryMethod(category.category_id)" class="btn btn-outline-dark"><i class="fa-solid fa-trash"></i></button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

    </div>
    <!-- /.container-fluid -->

    <!-- Modal para crear / editar categoría -->
    <div class="modal fade" id="categoryModal" tabindex="-1" aria-labelledby="categoryModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <!-- Título cambia según el modo (crear o editar) -->
            <h5 class="modal-title" id="categoryModalLabel">{{ isEditMode ? 'Editar Categoría' : 'Registrar Categoría' }}</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="isEditMode ? updateCategory() : registerCategory()">
                <div class="mb-3">
                    <label for="categoryName" class="form-label">Nombre</label>
                    <input type="text" id="categoryName" class="form-control" v-model="currentCategory.category_name" required>
                </div>
                <div class="mb-3">
                    <label for="categoryDescription" class="form-label">Descripción</label>
                    <textarea id="categoryDescription" class="form-control" v-model="currentCategory.category_description" required></textarea>
                </div>
                <!-- Botón de enviar (guardar o registrar) según isEditMode -->
                <button type="submit" class="btn btn-primary">{{ isEditMode ? 'Guardar Cambios' : 'Registrar Categoría' }}</button>
            </form>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
// Importar los metodos del archivo /services/categoryService para hacer peticiones a la API
import { deleteCategory, getAllActiveCategories, updateCategory, createCategory, setCategoryStatus } from '@/services/categoryService';

export default {
    data() {
        return {
            categories: [],  // Lista de categorías
            currentCategory: {},  // Categoría actual para crear o editar
            isEditMode: false,  // Indica si estamos en modo edición o creación
        }
    },
    methods: {
        // Obtiene las categorías de la página actual
        async fetchCategories() {
            try {
                const response = await getAllActiveCategories();
                this.categories = response.data; // Asigna las categorías obtenidas
                
            } catch (error) {
                alert(error.data.detail);
            }
        },

        // Elimina una categoría
        async deleteCategoryMethod(categoryId) {
            if (confirm('¿Estás seguro de que deseas eliminar esta categoría?')) {
                try {
                    await deleteCategory(categoryId);
                    alert('Categoría eliminada exitosamente');
                    this.fetchCategories();
                } catch (error) {
                    alert(error.data.detail);
                }
            }
        },

        // Abre el modal para registrar una nueva categoría
        openCreateModal() {
            this.currentCategory = { name: '', description: '' }; // Inicializa la categoría vacía
            this.isEditMode = false; // Cambia el modo a crear
            $('#categoryModal').modal('show'); // Abre el modal
        },

        // Abre el modal para editar una categoría
        openEditModal(category) {
            this.currentCategory = { ...category }; // Clona la categoría seleccionada
            this.isEditMode = true; // Cambia el modo a editar
            $('#categoryModal').modal('show'); // Abre el modal
        },

        // Registra una nueva categoría llamando a la API
        async registerCategory() {
            try {
                await createCategory(this.currentCategory.category_name, this.currentCategory.category_description);
                alert('Categoría registrada exitosamente');
                this.fetchCategories();
                $('#categoryModal').modal('hide');
            } catch (error) {
                alert(error.data.detail);
            }
        },

        // Actualiza una categoría llamando a la API
        async updateCategory() {
            try {
                await updateCategory(this.currentCategory.category_id, this.currentCategory.category_name, this.currentCategory.category_description);
                alert('Categoría actualizada exitosamente');
                this.fetchCategories();
                $('#categoryModal').modal('hide');
            } catch (error) {
                alert(error.data.detail);
            }
        },

        toggleCategoryStatus(category) {
            // Cambiar el valor del estado
            category.category_status = category.category_status == 1 ? 0 : 1;
            // Si necesitas actualizar el backend con el nuevo estado:
            this.updateCategoryStatus(category.category_id, category.category_status);
        },

        // Actualizar el estado de la categoria
        async updateCategoryStatus(id, theStatus) {
            if (confirm('¿Estás seguro de que deseas cambiar el estado de la categoría?')) {
                try {
                    await setCategoryStatus(id, theStatus);
                    alert('El estado de la Categoría, actualizado exitosamente');
                    this.fetchCategories();
                } catch (error) {
                    alert(error.data.detail);
                }
            }
        },
    },
    mounted() {
        this.fetchCategories(); // Llama al método para obtener las categorías al cargar este componente
    },
}
</script>
