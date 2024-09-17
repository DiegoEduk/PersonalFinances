import api from './api';

// Función para crear una nueva categoría
export const createCategory = async (categoryName, categoryDescription) => {
  try {
    const response = await api.post('/category/create', {
      category_name: categoryName,  
      category_description: categoryDescription
    });
    return response;
  } catch (error) {
    if (error.response) {
      throw error.response; // Devuelve el error original de la API
    } else {
      throw new Error('Error de red o de servidor');
    }
  }
};

// Función para obtener una categoría por su ID
export const getCategoryById = async (categoryId) => {
  try {
    const response = await api.get(`/category/get-by-id/${categoryId}`);
    return response;
  } catch (error) {
    if (error.response) {
      throw error.response; // Devuelve el error original de la API
    } else {
      throw new Error('Error de red o de servidor');
    }
  }
};

// Función para obtener todas las categorías activas
export const getAllActiveCategories = async () => {
  try {
    const response = await api.get('/category/get-all');
    return response;
  } catch (error) {
    if (error.response) {
      throw error.response; // Devuelve el error original de la API
    } else {
      throw new Error('Error de red o de servidor');
    }
  }
};

// Función para actualizar una categoría
export const updateCategory = async (categoryId, categoryName, categoryDescription) => {
  try {
    const response = await api.put(`/category/update/${categoryId}`, {
      category_name: categoryName,
      category_description: categoryDescription
    });
    return response;
  } catch (error) {
    if (error.response) {
      throw error.response; // Devuelve el error original de la API
    } else {
      throw new Error('Error de red o de servidor');
    }
  }
};

// Función para eliminar una categoría
export const deleteCategory = async (categoryId) => {
  try {
    const response = await api.delete(`/category/delete/${categoryId}`);
    return response;
  } catch (error) {
    if (error.response) {
      throw error.response; // Devuelve el error original de la API
    } else {
      throw new Error('Error de red o de servidor');
    }
  }
};

// Función para cambiar el estado (activo/inactivo) de una categoría
export const setCategoryStatus = async (categoryId, isActive) => {
  try {
    const response = await api.put(`/category/status/${categoryId}`, null, {
      params: { is_active: isActive }
    });
    return response;
  } catch (error) {
    if (error.response) {
      throw error.response; // Devuelve el error original de la API
    } else {
      throw new Error('Error de red o de servidor');
    }
  }
};

// Función para obtener una categoría por su nombre
export const getCategoryByName = async (categoryName) => {
  try {
    const response = await api.get(`/category/get-by-name/${categoryName}`);
    return response;
  } catch (error) {
    if (error.response) {
      throw error.response; // Devuelve el error original de la API
    } else {
      throw new Error('Error de red o de servidor');
    }
  }
};
