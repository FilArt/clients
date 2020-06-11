<template>
  <v-tooltip bottom>
    <template v-slot:activator="{ on }">
      <v-btn
        v-on="on"
        :icon="!label"
        :disabled="disabled"
        :block="block"
        color="success"
        @click="$emit('click')"
      >
        {{ label }}
        <v-icon :right="!!label">mdi-check</v-icon>
      </v-btn>
    </template>
    <span>{{ label ? label : 'Submit' }}</span>
  </v-tooltip>
</template>

<script>
export default {
  name: 'submitButton',
  props: {
    disabled: {
      type: Boolean,
      default: false,
    },
    block: {
      type: Boolean,
      default: false,
    },
    label: {
      type: String,
      default: null,
    },
  },
}
</script>
