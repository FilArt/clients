<template>
  <v-tooltip bottom>
    <template v-slot:activator="{ on }">
      <v-btn icon color="success" :loading="loading" :disabled="disabled" v-on="on" @click="$emit('click')">
        <v-icon>mdi-refresh</v-icon>
      </v-btn>
    </template>
    <span>Refresh</span>
  </v-tooltip>
</template>

<script>
export default {
  name: 'RefreshButton',
  props: {
    loading: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
}
</script>
