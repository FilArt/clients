<template>
  <v-tooltip bottom>
    <template v-slot:activator="{ on }">
      <v-btn
        v-on="on"
        icon
        color="success"
        @click="$emit('click')"
        :loading="loading"
        :disabled="disabled"
      >
        <v-icon>mdi-refresh</v-icon>
      </v-btn>
    </template>
    <span>Refresh</span>
  </v-tooltip>
</template>

<script>
export default {
  name: 'refreshButton',
  props: {
    loading: {
      type: Boolean,
      default: false
    },
    disabled: {
      type: Boolean,
      default: false
    }
  }
}
</script>
