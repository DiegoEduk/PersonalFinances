<template>
  <MiComponenteSlot>
    <template #header>
      <div class="row py-5">
        <VModel></VModel>
      </div>
      <MiContador></MiContador>
      <LogoSena></LogoSena>
      <h1>Esto es el Header de mi sitio</h1>
      <MiUsuario></MiUsuario>
    </template>
    <div class="row">
      <VerifyLoggin></VerifyLoggin>
    </div>
    <div class="row">
      <HelloWorld msg="Estrella" texto="este es un texto de la estrella" texto_enlace="Fugaz" />
      <HelloWorld msg="Luna" texto="este es un texto de la luna" texto_enlace="Llena" />
      <HelloWorld msg="Sol" texto="este es un texto del sol" texto_enlace="Ardiente" />
      <HelloWorld msg="Jupiter" texto="este es un texto de jupiter" texto_enlace="Grande" />
    </div>
    <template #footer>
      <div class="container">
        <div class="row bg-black text-white py-4">
          <MisProductos></MisProductos>
        </div>
        <MiBoton @mensaje-enviado="mostrarMensaje" />
      </div>
    </template>
  </MiComponenteSlot>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import LogoSena from './components/LogoSena.vue';
import MiBoton from './components/MiBoton.vue';
import MiComponenteSlot from './components/MiComponenteSlot.vue';
import MiContador from './components/MiContador.vue';
import MisProductos from './components/MisProductos.vue';
import MiUsuario from './components/MiUsuario.vue';
import VerifyLoggin from './components/VerifyLoggin.vue';
import VModel from './components/VModel.vue';

export default {
  name: 'App',
  components: {
    HelloWorld,
    MiBoton,
    MiComponenteSlot,
    MiContador,
    MiUsuario,
    LogoSena,
    VerifyLoggin,
    MisProductos,
    VModel
  },
  methods: {
    mostrarMensaje(mensaje) {
      alert(mensaje);
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
