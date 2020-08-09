<template>
  <v-btn :nuxt="!!to" :to="to" rounded block color="primary" @click="$emit('click')">
    Atrás
    <v-icon>mdi-keyboard-return</v-icon>
  </v-btn>
</template>

<script>
export default {
  name: 'ReturnButton',
  props: {
    to: {
      type: String,
      default: '/',
    },
  },
}
</script>
