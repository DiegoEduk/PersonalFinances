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
                                <th>Fecha de Creación</th>
                                <th>Última Actualización</th>
                                <th></th>
                            </tr>
                        </thead>

                        <tbody>
                            <!-- Recorre la lista de categorías con v-for -->
                            <tr v-for="category in categories" :key="category.id">
                                <!-- Muestra los datos de cada categoría en cada td-->
                                <td>{{ category.name }}</td>
                                <td>{{ category.description }}</td>
                                <td>{{ formatDate(category.created_at) }}</td>
                                <td>{{ formatDate(category.updated_at) }}</td>
                                <!-- Botones para editar o eliminar una categoría -->
                                <td>
                                    <button @click="openEditModal(category)" class="btn btn-outline-secondary"><i
                                            class="fa-solid fa-pen-to-square"></i></button>
                                    <button @click="deleteCategoryMethod(category.id)" class="btn btn-outline-dark"><i class="fa-solid fa-trash"></i></button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Controles de paginación -->
                <div class="pagination-controls">
                    <!-- Botón para la página anterior, con click llama a la función prevPage  -->
                    <button class="btn btn-primary m-3" @click="prevPage" :disabled="currentPage === 1">Anterior</button>
                    <!-- Muestra la página actual y total de páginas -->
                    <span>Página {{ currentPage }} de {{ totalPages }}</span>
                    <!-- Botón para la página siguiente,  con click llama a la función nextPage -->
                    <button class="btn btn-primary m-3" @click="nextPage" :disabled="currentPage === totalPages">Siguiente</button>
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
                    <input type="text" id="categoryName" class="form-control" v-model="currentCategory.name" required>
                </div>
                <div class="mb-3">
                    <label for="categoryDescription" class="form-label">Descripción</label>
                    <textarea id="categoryDescription" class="form-control" v-model="currentCategory.description" required></textarea>
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
import { getCategoriesByPage, deleteCategory, updateCategory, createCategory } from '@/services/categoryService';

export default {
    data() {
        return {
            categories: [],  // Lista de categorías
            currentCategory: {},  // Categoría actual para crear o editar
            currentPage: 1,  // Página actual para la paginación
            totalPages: 0,  // Total de páginas
            isEditMode: false,  // Indica si estamos en modo edición o creación
        }
    },
    methods: {
        // Obtiene las categorías de la página actual
        async fetchCategories() {
            try {
                const response = await getCategoriesByPage(this.currentPage);
                this.categories = response.data.categories; // Asigna las categorías obtenidas
                this.totalPages = response.data.total_pages; // Asigna el total de páginas
            } catch (error) {
                alert(error.data.detail);
            }
        },

        // Función para ir a la página siguiente
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
                this.fetchCategories();
            }
        },

        // Función para ir a la página anterior
        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
                this.fetchCategories();
            }
        },

        // Formatea una fecha para mostrarla de manera legible
        formatDate(dateString) {
            const options = {
                year: 'numeric',
                month: 'numeric',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            };
            return new Date(dateString).toLocaleDateString('es-ES', options);
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
                await createCategory(this.currentCategory.name, this.currentCategory.description);
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
                await updateCategory(this.currentCategory.id, this.currentCategory.name, this.currentCategory.description);
                alert('Categoría actualizada exitosamente');
                this.fetchCategories();
                $('#categoryModal').modal('hide');
            } catch (error) {
                alert(error.data.detail);
            }
        },
    },
    mounted() {
        this.fetchCategories(); // Llama al método para obtener las categorías al cargar este componente
    },
}
</script>
