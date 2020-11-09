<template>
  <v-tooltip bottom>
    <template v-slot:activator="{ on }">
      <v-btn
        type="submit"
        :icon="!label"
        :disabled="disabled"
        :block="block"
        color="primary"
        v-on="on"
        @click="$emit('click')"
      >
        {{ label }}
        <v-icon :right="!!label"> mdi-check </v-icon>
      </v-btn>
    </template>
    <span>{{ label ? label : 'Enviar' }}</span>
  </v-tooltip>
</template>

<script>
export default {
  name: 'SubmitButton',
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
