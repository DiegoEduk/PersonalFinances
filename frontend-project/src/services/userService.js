import api from './api'; // Asegúrate de que `api.js` esté configurado adecuadamente

// Función para crear un nuevo usuario
export const createUser = async (fullName, email, userRole, passhash) => {
  try {
    const response = await api.post('/users/create', {
      full_name: fullName,
      mail: email,
      user_role: userRole,
      passhash: passhash
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}` // Incluye el token de autenticación
      }
    });
    return response;
  } catch (error) {
    if (error.response) {
      throw error; // Lanza el error para que lo maneje el store
    } else {
      throw new Error('Error de red o de servidor'); // Manejar errores de red
    }
  }
};

// Función para obtener un usuario por su email
export const getUserByEmail = async (email) => {
  try {
    const response = await api.get(`/users/get-user-by-email/?email=${encodeURIComponent(email)}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}` // Incluye el token de autenticación
      }
    });
    return response;
  } catch (error) {
    if (error.response) {
      throw error; // Lanza el error para que lo maneje el store
    } else {
      throw new Error('Error de red o de servidor'); // Manejar errores de red
    }
  }
};

// Función para obtener todos los usuarios con paginación
export const getUsersByPage = async (page = 1, pageSize = 10) => {
  try {
    const response = await api.get(`/users/users-by-page/?page=${page}&page_size=${pageSize}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}` // Incluye el token de autenticación
      }
    });
    return response;
  } catch (error) {
    if (error.response) {
      throw error; // Lanza el error para que lo maneje el store
    } else {
      throw new Error('Error de red o de servidor'); // Manejar errores de red
    }
  }
};

// Función para actualizar un usuario
export const updateUser = async (userId, fullName, email, userRole, userStatus) => {
  try {
    const response = await api.put(`/users/update/?user_id=${userId}`, {
      full_name: fullName,
      mail: email,
      user_role: userRole,
      user_status: userStatus
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}` // Incluye el token de autenticación
      }
    });
    return response;
  } catch (error) {
    if (error.response) {
      throw error; // Lanza el error para que lo maneje el store
    } else {
      throw new Error('Error de red o de servidor'); // Manejar errores de red
    }
  }
};

// Función para eliminar un usuario
export const deleteUser = async (userId) => {
  try {
    const response = await api.delete(`/users/delete/${userId}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('access_token')}` // Incluye el token de autenticación
      }
    });
    return response;
  } catch (error) {
    if (error.response) {
      throw error; // Lanza el error para que lo maneje el store
    } else {
      throw new Error('Error de red o de servidor'); // Manejar errores de red
    }
  }
};
