<template>
  <v-tooltip bottom>
    <template v-slot:activator="{ on }">
      <v-btn
        v-on="on"
        icon
        color="success"
        :disabled="disabled"
        @click="$emit('click')"
      >
        <v-icon>mdi-check</v-icon>
      </v-btn>
    </template>
    <span>Submit</span>
  </v-tooltip>
</template>

<script>
export default {
  name: 'submitButton',
  props: {
    disabled: {
      type: Boolean,
      default: false
    }
  }
}
</script>
