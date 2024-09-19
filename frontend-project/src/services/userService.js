import api from './api'; 

// Función para crear un nuevo usuario con un archivo de imagen
export const createUser = async (fullName, email, userRole, passhash, fileImg) => {
  try {
    // Crea un objeto FormData para manejar multipart/form-data
    const formData = new FormData();
    formData.append('full_name', fullName);
    formData.append('mail', email);
    formData.append('user_role', userRole);
    formData.append('passhash', passhash);
    formData.append('file_img', fileImg); // Archivo de imagen

    // No necesitas pasar el token, ya que el interceptor lo añade automáticamente
    const response = await api.post('/users/create', formData, {
      headers: {
        'Content-Type': 'multipart/form-data', // Asegúrate de que el encabezado es multipart/form-data
      },
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

// Función para obtener un usuario por su email
export const getUserByEmail = async (email) => {
  try {
    const response = await api.get(`/users/get-user-by-email/?email=${encodeURIComponent(email)}`);
    return response;
  } catch (error) {
    if (error.response) {
      throw error.response; // Devuelve el error original de la API
    } else {
      throw new Error('Error de red o de servidor'); // Manejar errores de red
    }
  }
};

// Función para obtener todos los usuarios con paginación
export const getUsersByPage = async (page = 1, pageSize = 10) => {
  try {
    const response = await api.get(`/users/users-by-page/?page=${page}&page_size=${pageSize}`);
    return response;
  } catch (error) {
    if (error.response) {
      throw error.response; // Devuelve el error original de la API
    } else {
      throw new Error('Error de red o de servidor');
    }
  }
};

// Función para actualizar un usuario
export const updateUser = async (userId, fullName, email, userRole, imageFile = null) => {
  try {
    const formData = new FormData();
    formData.append('full_name', fullName);
    formData.append('mail', email);
    formData.append('user_role', userRole);

    // Si se proporciona una imagen, agregarla al FormData
    if (imageFile) {
      formData.append('file_img', imageFile);
    }

    const response = await api.put(`/users/update/?user_id=${userId}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Bearer ${localStorage.getItem('accessToken')}` // Asegúrate de obtener el token correctamente
      }
    });

    return response;
  } catch (error) {
    if (error.response) {
      throw error.response; // Devuelve el error original de la API
    } else {
      throw new Error('Error de red o de servidor'); // Manejar errores de red
    }
  }
};

// Función para eliminar un usuario
export const deleteUser = async (userId) => {
  try {
    const response = await api.delete(`/users/delete/${userId}`);
    return response;
  } catch (error) {
    if (error.response) {
      throw error.response; // Devuelve el error original de la API
    } else {
      throw new Error('Error de red o de servidor'); // Manejar errores de red
    }
  }
};
