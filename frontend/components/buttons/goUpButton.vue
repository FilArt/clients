<template>
  <v-btn
    fab
    x-large
    icon
    large
    fixed
    bottom
    right
    color="yellow"
    @click="$vuetify.goTo(0)"
  >
    <v-icon>mdi-arrow-up</v-icon>
  </v-btn>
</template>

<script>
export default {
  name: 'goUpButton',
}
</script>
