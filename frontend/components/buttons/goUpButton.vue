<template>
  <v-btn fab outlined icon large fixed bottom right color="yellow" @click="$vuetify.goTo(0)">
    <v-icon>mdi-arrow-up</v-icon>
  </v-btn>
</template>

<script>
export default {
  name: 'GoUpButton',
}
</script>
