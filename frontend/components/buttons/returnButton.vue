<template>
  <v-tooltip bottom>
    <template v-slot:activator="{ on }">
      <v-btn nuxt :to="to" rounded block outlined color="info">
        Back
        <v-icon>mdi-keyboard-return</v-icon>
      </v-btn>
    </template>
    <span>Cancel</span>
  </v-tooltip>
</template>

<script>
export default {
  name: 'returnButton',
  props: {
    to: {
      type: String,
      default: '/'
    }
  }
}
</script>
