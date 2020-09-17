<template>
  <v-snackbar v-model="snackbar" right bottom :timeout="timeout" color="success">
    {{ title }}

    <template v-slot:action="{ attrs }">
      <v-btn text v-bind="attrs" @click="snackbar = false"> Cerrar </v-btn>
    </template>
  </v-snackbar>
</template>
<script>
export default {
  name: 'SnackBarIt',
  props: {
    notyKey: {
      type: Number,
      default: 0,
    },
    title: {
      type: String,
      default: 'Listo!',
    },
    timeout: {
      type: Number,
      default: 2500,
    },
  },
  data() {
    return {
      snackbar: false,
    }
  },
  watch: {
    notyKey() {
      this.snackbarit()
    },
  },
  methods: {
    snackbarit(title) {
      if (this.snackbar) this.snackbar = false
      this.snackbarTitle = title || 'Listo!'
      this.snackbar = true
    },
  },
}
</script>
