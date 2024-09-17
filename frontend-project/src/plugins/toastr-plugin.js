// src/plugins/toastr-plugin.js
import toastr from 'toastr';
import 'toastr/build/toastr.min.css';

const ToastrPlugin = {
  install(Vue) {
    // Configuración global de Toastr
    toastr.options = {
      closeButton: true,
      debug: false,
      newestOnTop: false,
      progressBar: true,
      positionClass: 'toast-top-right',
      preventDuplicates: false,
      onclick: null,
      showDuration: '300',
      hideDuration: '1000',
      timeOut: '5000',
      extendedTimeOut: '1000',
      showEasing: 'swing',
      hideEasing: 'linear',
      showMethod: 'fadeIn',
      hideMethod: 'fadeOut'
    };

    // Añade Toastr a Vue.prototype para que esté disponible en todos los componentes
    Vue.prototype.$toastr = toastr;
  }
};

export default ToastrPlugin;
