import api from './api';

// Función para crear una nueva transacción
export const createTransaction = async (transactionData) => {
  try {
    const response = await api.post('/transaction/create', transactionData);
    return response;
  } catch (error) {
    if (error.response) {
      throw error.response; // Devuelve el error de la API
    } else {
      throw new Error('Error de red o de servidor');
    }
  }
};

// Función para actualizar una transacción por ID
export const updateTransaction = async (transactionId, transactionData) => {
  try {
    const response = await api.put(`/transaction/update/${transactionId}`, transactionData);
    return response;
  } catch (error) {
    if (error.response) {
      throw error.response; // Devuelve el error de la API
    } else {
      throw new Error('Error de red o de servidor');
    }
  }
};

// Función para eliminar una transacción por ID
export const deleteTransaction = async (transactionId) => {
  try {
    const response = await api.delete(`/transaction/delete/${transactionId}`);
    return response;
  } catch (error) {
    if (error.response) {
      throw error.response; // Devuelve el error de la API
    } else {
      throw new Error('Error de red o de servidor');
    }
  }
};

// Función para obtener transacciones por usuario y fechas
export const getTransactionsByUserAndDate = async (userId, startDate, endDate) => {
  try {
    const response = await api.get('/transaction/get-by-user-and-date', {
      params: {
        user_id: userId,
        start_date: startDate,
        end_date: endDate,
      },
    });
    return response;
  } catch (error) {
    if (error.response) {
      throw error.response; // Devuelve el error de la API
    } else {
      throw new Error('Error de red o de servidor');
    }
  }
};

// Función para subir un archivo relacionado con una transacción
export const uploadTransactionFile = async (transactionId, file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post(`/transaction/upload-file/?transactions_id=${transactionId}`, formData, {
      'Content-Type': 'multipart/form-data',
    });
    return response;
  } catch (error) {
    if (error.response) {
      throw error.response; // Devuelve el error de la API
    } else {
      throw new Error('Error de red o de servidor');
    }
  }
};
