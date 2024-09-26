<template>
    <div class="container-fluid">
        <!-- Título de la página -->
        <h1 class="h3 mb-2 text-gray-800">Transacciones</h1>

        <div class="row mb-3">
            <div class="col-3">
                <!-- Botón para registrar una nueva transacción -->
                <button @click="openCreateModal" class="btn btn-success">Registrar Transacción</button>
            </div>
            <div class="col-3">
                <!-- Selección de rango de fechas -->
                <div class="mr-3">
                    <input type="date" id="startDate" v-model="startDate" class="form-control">
                </div>
            </div>
            <div class="col-3">
                <div class="mr-3">
                    <input type="date" id="endDate" v-model="endDate" class="form-control">
                </div>
            </div>
            <div class="col-3">
                <!-- Botón para buscar transacciones en el rango seleccionado -->
                <button @click="fetchTransactions" class="btn btn-primary mr-3">Buscar</button>
            </div>
        </div>

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
                                <th>Categoría</th>
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
            </div>
        </div>

        <!-- Modal para crear / editar transacción -->
        <div class="modal fade" id="transactionModal" tabindex="-1" aria-labelledby="transactionModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="transactionModalLabel">{{ isEditMode ? 'Editar Transacción' : 'Registrar Transacción' }}</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <div class="row">
                            <div class="col-6">
                                <form @submit.prevent="isEditMode ? updateTransactionMethod() : registerTransaction()">
                                    <div class="mb-3">
                                        <label for="description" class="form-label">Descripción</label>
                                        <input type="text" id="description" class="form-control" v-model="currentTransaction.t_description" required>
                                    </div>
                                    <div class="mb-3">
                                        <label for="amount" class="form-label">Monto</label>
                                        <input type="number" id="amount" class="form-control" v-model="currentTransaction.amount" required>
                                    </div>
                                    <div class="mb-3">
                                        <label for="type" class="form-label">Tipo</label>
                                        <select v-model="currentTransaction.t_type" class="form-control" required>
                                            <option value="revenue">Ingreso</option>
                                            <option value="expenses">Gasto</option>
                                        </select>
                                    </div>
                                    <div class="mb-3">
                                        <label for="category" class="form-label">Categoría</label>
                                        <!-- Pasar la categoría seleccionada actual al componente CategorySelect -->
                                        <CategorySelect :selected-category-id="currentTransaction.category_id" @category-selected="updateTransactionCategory" />
                                    </div>
                                    <div class="mb-3">
                                        <label for="date" class="form-label">Fecha</label>
                                        <input type="date" id="date" class="form-control" v-model="currentTransaction.t_date" required>
                                    </div>
                                    <button type="submit" class="btn btn-primary">{{ isEditMode ? 'Guardar Cambios' : 'Registrar Transacción' }}</button>
                                </form>
                            </div>
                            <div class="col-6">
                                <form @submit.prevent="uploadTransactionFiles()">
                                     <!-- Campo para subir archivo relacionado con la transacción -->
                                    <div class="mb-3">
                                        <label for="fileUpload" class="form-label">Subir Archivo</label>
                                        <input type="file" id="fileUpload" class="form-control" @change="handleFileChange">
                                    </div>
                                    <button type="submit" class="btn btn-primary">Almacenar Archivo</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
// Importar los servicios del archivo transactionServices
import { getTransactionsByUserAndDate, createTransaction, updateTransaction, deleteTransaction, uploadTransactionFile } from '@/services/transactionServices';
import CategorySelect from '../Category/CategorySelect.vue';
import { useAuthStore } from '@/store/'; // Store de autenticación para obtener el user_id

export default {
    data() {
        return {
            transactions: [],  // Lista de transacciones
            currentTransaction: {},  // Transacción actual para crear o editar
            isEditMode: false,  // Indica si estamos en modo edición o creación
            startDate: '',  // Fecha de inicio para la búsqueda personalizada
            endDate: '',  // Fecha de fin para la búsqueda personalizada
            selectedFile: null, // Para almacenar el archivo seleccionado
            transactionFiles: [],
        };
    },
    components: {
        CategorySelect, // Registra el componente CategorySelect
    },
    methods: {
        // Método para manejar la selección del archivo
        handleFileChange(event) {
            this.selectedFile = event.target.files[0]; // Almacena el archivo seleccionado
        },

        // Método para subir el archivo relacionado con la transacción
        async uploadTransactionFiles() {
            try {
                if (this.selectedFile) {
                    await uploadTransactionFile(this.currentTransaction.transactions_id, this.selectedFile); // Llama al servicio para subir el archivo
                    alert('Archivo subido exitosamente');
                }
            } catch (error) {
                console.error('Error al subir el archivo:', error);
            }
        },

        // Obtiene las transacciones del usuario por fecha
        async fetchTransactions() {
            try {
                const authStore = useAuthStore();  // Obtener el user_id del store
                const userId = authStore.user?.user_id || '';

                // Si no se han seleccionado fechas, usamos el mes actual
                const currentDate = new Date();
                const defaultStartDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1).toISOString().split('T')[0];
                const defaultEndDate = currentDate.toISOString().split('T')[0];

                const start = this.startDate || defaultStartDate;
                const end = this.endDate || defaultEndDate;

                const response = await getTransactionsByUserAndDate(userId, start, end);
                this.transactions = response.data || []; // Asigna las transacciones obtenidas
                
            } catch (error) {
                console.error('Error al cargar las transacciones:', error);
            }
        },

        // Registra una nueva transacción llamando a la API
        async registerTransaction() {
            try {
                const authStore = useAuthStore();  // Obtener el user_id del store
                const userId = authStore.user?.user_id || '';
                
                await createTransaction(
                    userId,
                    this.currentTransaction.category_id,
                    this.currentTransaction.amount,
                    this.currentTransaction.t_description,
                    this.currentTransaction.t_type,
                    this.currentTransaction.t_date
                );

                alert('Transacción registrada exitosamente');
                this.fetchTransactions(); // Refresca la lista de transacciones después de registrar
                $('#transactionModal').modal('hide'); // Cierra el modal
            } catch (error) {
                console.error('Error al registrar la transacción:', error);
            }
        },

        // Actualiza una transacción llamando a la API
        async updateTransactionMethod() {
            try {
                await updateTransaction(
                    this.currentTransaction.transactions_id,
                    this.currentTransaction.category_id,
                    this.currentTransaction.amount,
                    this.currentTransaction.t_description,
                    this.currentTransaction.t_type,
                    this.currentTransaction.t_date
                );
                alert('Transacción actualizada exitosamente');
                this.fetchTransactions(); // Refresca la lista de transacciones después de actualizar
                $('#transactionModal').modal('hide'); // Cierra el modal
            } catch (error) {
                console.error('Error al actualizar la transacción:', error);
            }
        },

        // Elimina una transacción
        async deleteTransactionMethod(transactionId) {
            if (confirm('¿Estás seguro de que deseas eliminar esta transacción?')) {
                try {
                    await deleteTransaction(transactionId);
                    alert('Transacción eliminada exitosamente');
                    this.fetchTransactions(); // Refresca la lista de transacciones después de eliminar
                } catch (error) {
                    console.error('Error al eliminar la transacción:', error);
                }
            }
        },

        // Abre el modal para registrar una nueva transacción
        openCreateModal() {
            this.currentTransaction = { t_description: '', amount: 0, t_type: 'expenses', t_date: '', category_id: null }; // Inicializa la transacción vacía
            this.isEditMode = false; // Cambia el modo a creación
            $('#transactionModal').modal('show'); // Abre el modal
        },

        // Abre el modal para editar una transacción
        openEditModal(transaction) {
            this.currentTransaction = { ...transaction }; // Clona la transacción seleccionada
            this.isEditMode = true; // Cambia el modo a edición
            $('#transactionModal').modal('show'); // Abre el modal
        },

        // Actualiza la categoría seleccionada en `currentTransaction`
        updateTransactionCategory(selectedCategory) {
            this.currentTransaction.category_id = selectedCategory;
        },

        // Formatea una fecha para mostrarla de manera legible
        formatDate(dateString) {
            const options = {
                year: 'numeric',
                month: 'numeric',
                day: 'numeric'
            };
            return new Date(dateString).toLocaleDateString('es-ES', options);
        },

        // Formatea el monto como moneda
        formatCurrency(amount) {
            return new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'COP' }).format(amount);
        },
    },
    mounted() {
        this.fetchTransactions(); // Llama al método para obtener las transacciones al cargar el componente
    },
};
</script>
