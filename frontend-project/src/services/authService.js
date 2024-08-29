import api from './api'; 

// Función para manejar el inicio de sesión
export const login = async (username, password) => {
  try {
    // Enviar solicitud de inicio de sesión
    const response = await api.post('/access/token', new URLSearchParams({
      grant_type: '',
      username,
      password,
      scope: '',
      client_id: '',
      client_secret: ''
    }), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    
    // Retornar la respuesta de la API
    return response;
  } catch (error) {
    // Manejar errores de la solicitud
    if (error.response) {
      throw error; // Lanza el error para que lo maneje el store
    } else {
      throw new Error('Error de red o de servidor'); // Manejar errores de red
    }
  }
};

// Función para manejar el registro de un nuevo usuario
export const register = async (fullName, email, userRole, password) => {
  try {
    // Enviar solicitud de registro
    const response = await api.post('/access/register', {
      full_name: fullName,
      mail: email,
      user_role: userRole,
      passhash: password
    }, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    // Retornar la respuesta de la API
    return response;
  } catch (error) {
    // Manejar errores de la solicitud
    if (error.response) {
      throw error; // Lanza el error para que lo maneje el store
    } else {
      throw new Error('Error de red o de servidor'); // Manejar errores de red
    }
  }
};

// Otros servicios relacionados con autenticación pueden ser añadidos aquí
