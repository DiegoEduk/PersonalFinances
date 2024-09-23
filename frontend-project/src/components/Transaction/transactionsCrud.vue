<template>
    <div class="container-fluid">
        <!-- Título de la página -->
        <h1 class="h3 mb-2 text-gray-800">Transacciones del Mes</h1>

        <!-- Botón para registrar una nueva transacción -->
        <button @click="openCreateModal" class="btn btn-success mb-4">Registrar Nueva Transacción</button>

        <!-- Tabla de Transacciones -->
        <div class="card shadow mb-4">
            <div class="card-header py-3">
                <h6 class="m-0 font-weight-bold text-primary">Lista de Transacciones</h6>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
                        <thead>
                            <tr>
                                <th>Descripción</th>
                                <th>Monto</th>
                                <th>Tipo</th>
                                <th>Categoria</th>
                                <th>Fecha</th>
                                <th></th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr v-for="transaction in transactions" :key="transaction.transactions_id">
                                <td>{{ transaction.t_description }}</td>
                                <td>{{ formatCurrency(transaction.amount) }}</td>
                                <td>{{ transaction.t_type === 'revenue' ? 'Ingreso' : 'Gasto' }}</td>
                                <td>{{ transaction.category_name }}</td>
                                <td>{{ formatDate(transaction.t_date) }}</td>
                                <td>
                                    <button @click="openEditModal(transaction)" class="btn btn-outline-secondary">
                                        <i class="fa-solid fa-pen-to-square"></i>
                                    </button>
                                    <button @click="deleteTransactionMethod(transaction.transactions_id)" class="btn btn-outline-dark">
                                        <i class="fa-solid fa-trash"></i>
                                    </button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Controles de paginación -->
                <div class="pagination-controls">
                    <button class="btn btn-primary m-3" @click="prevPage" :disabled="currentPage === 1">Anterior</button>
                    <span>Página {{ currentPage }} de {{ totalPages }}</span>
                    <button class="btn btn-primary m-3" @click="nextPage" :disabled="currentPage === totalPages">Siguiente</button>
                </div>
            </div>
        </div>

        <!-- Modal para crear/editar transacción -->
        <div class="modal fade" id="transactionModal" tabindex="-1" aria-labelledby="transactionModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="transactionModalLabel">{{ isEditMode ? 'Editar Transacción' : 'Registrar Nueva Transacción' }}</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="isEditMode ? updateTransaction() : createTransaction()">
                            <!-- Campo para la descripción -->
                            <div class="mb-3">
                                <label for="description" class="form-label">Descripción</label>
                                <input type="text" v-model="currentTransaction.t_description" class="form-control" required>
                            </div>
                            <!-- Campo para el monto -->
                            <div class="mb-3">
                                <label for="amount" class="form-label">Monto</label>
                                <input type="number" v-model="currentTransaction.amount" class="form-control" required>
                            </div>
                            <!-- Selección del tipo de transacción -->
                            <div class="mb-3">
                                <label for="type" class="form-label">Tipo</label>
                                <select v-model="currentTransaction.t_type" class="form-control" required>
                                    <option value="revenue">Ingreso</option>
                                    <option value="expenses">Gasto</option>
                                </select>
                            </div>
                            <!-- Selección de la categoría con el componente CategorySelect -->
                            <div class="mb-3">
                                <label for="category" class="form-label">Categoría</label>
                                <CategorySelect @category-selected="handleCategorySelected" />
                            </div>
                            <!-- Campo para la fecha -->
                            <div class="mb-3">
                                <label for="date" class="form-label">Fecha</label>
                                <input type="date" v-model="currentTransaction.t_date" class="form-control" required>
                            </div>
                            <button type="submit" class="btn btn-primary">{{ isEditMode ? 'Guardar Cambios' : 'Registrar Transacción' }}</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { getTransactionsByUserAndDate, createTransaction, updateTransaction, deleteTransaction } from '@/services/transactionServices';
import { useAuthStore } from '@/store/'; // Store para acceder al user_id
import CategorySelect from '@/components/Category/CategorySelect.vue'; // Importar el componente hijo para seleccionar categoría

export default {
    components: {
        CategorySelect, // Registramos el componente hijo
    },
    setup() {
        const authStore = useAuthStore(); // Obtener el store de autenticación para acceder al user_id

        const transactions = ref([]); // Lista de transacciones
        const currentTransaction = ref({ t_description: '', amount: 0, t_type: 'expenses', t_date: '', category_id: null }); // Transacción actual
        const isEditMode = ref(false); // Modo creación o edición
        const currentPage = ref(1); // Página actual para la paginación
        const totalPages = ref(0); // Total de páginas
        const userId = authStore.user?.user_id || ''; // Obtener el user_id del store de autenticación
        const error = ref(null); // Mensaje de error

        // Función para obtener las transacciones del mes actual
        const fetchTransactions = async () => {
            try {
                const startDate = new Date(new Date().getFullYear(), new Date().getMonth(), 1).toISOString().split('T')[0];
                const endDate = new Date().toISOString().split('T')[0];

                const response = await getTransactionsByUserAndDate(userId, startDate, endDate);

                transactions.value = response.data || []; // Asignar las transacciones directamente
            } catch (err) {
                error.value = 'Error al cargar las transacciones.';
            }
        };

        // Función para crear una nueva transacción
        const createTransaction = async () => {
            try {
                await createTransaction(currentTransaction.value);
                fetchTransactions(); // Recarga las transacciones
                $('#transactionModal').modal('hide'); // Cierra el modal
            } catch (err) {
                error.value = 'Error al crear la transacción.';
            }
        };

        // Función para actualizar una transacción existente
        const updateTransaction = async () => {
            try {
                await updateTransaction(currentTransaction.value.transaction_id, currentTransaction.value);
                console.log(currentTransaction.value.transaction_id);
                console.log(currentTransaction.value);
                fetchTransactions(); // Recarga las transacciones
                $('#transactionModal').modal('hide'); // Cierra el modal
            } catch (err) {
                error.value = 'Error al actualizar la transacción.';
            }
        };

        // Función para eliminar una transacción
        const deleteTransactionMethod = async (transactionId) => {
            if (confirm('¿Estás seguro de que deseas eliminar esta transacción?')) {
                try {
                    await deleteTransaction(transactionId);
                    fetchTransactions(); // Recarga las transacciones
                } catch (err) {
                    error.value = 'Error al eliminar la transacción.';
                }
            }
        };

        // Abre el modal para registrar una nueva transacción
        const openCreateModal = () => {
            isEditMode.value = false;
            currentTransaction.value = { t_description: '', amount: 0, t_type: 'expenses', t_date: '', category_id: null }; // Inicializa una nueva transacción
            $('#transactionModal').modal('show'); // Abre el modal
        };

        // Abre el modal para editar una transacción existente
        const openEditModal = (transaction) => {
            isEditMode.value = true;
            currentTransaction.value = { ...transaction }; // Clona la transacción seleccionada
            $('#transactionModal').modal('show'); // Abre el modal
        };

        // Manejador para seleccionar la categoría
        const handleCategorySelected = (categoryId) => {
            currentTransaction.value.category_id = categoryId; // Asigna la categoría seleccionada
        };

        // Función para paginación
        const nextPage = () => {
            if (currentPage.value < totalPages.value) {
                currentPage.value++;
                fetchTransactions(); // Cargar la siguiente página
            }
        };

        const prevPage = () => {
            if (currentPage.value > 1) {
                currentPage.value--;
                fetchTransactions(); // Cargar la página anterior
            }
        };

        // Formatear fecha para mostrarla de manera legible
        const formatDate = (dateString) => {
            const options = { year: 'numeric', month: 'long', day: 'numeric' };
            return new Date(dateString).toLocaleDateString('es-ES', options);
        };

        // Formatear monto como moneda
        const formatCurrency = (amount) => {
            return new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'COP' }).format(amount);
        };

        onMounted(() => {
            fetchTransactions(); // Cargar las transacciones del mes actual al montar el componente
        });

        return {
            transactions,
            currentTransaction,
            isEditMode,
            fetchTransactions,
            createTransaction,
            updateTransaction,
            deleteTransactionMethod,
            openCreateModal,
            openEditModal,
            handleCategorySelected,
            nextPage,
            prevPage,
            currentPage,
            totalPages,
            formatDate,
            formatCurrency,
            error
        };
    }
};
</script>

<style scoped>
/* Estilos personalizados */
</style>
