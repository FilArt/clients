<template>
  <v-text-field v-model="modelValue" :label="label" :errors-messages="errorMessages" />
</template>

<script>
export default {
  name: 'DecimalField',
  props: {
    name: {
      type: String,
      default: '',
    },
    prefix: {
      type: String,
      default: '',
    },
    suffix: {
      type: String,
      default: '',
    },
    dense: {
      type: Boolean,
      default: false,
    },

    value: {
      type: [String, Number],
      default: 0,
    },
    label: {
      type: String,
      default: 'Numero',
    },
    errorMessages: {
      type: Array,
      default: () => [],
    },
  },
  computed: {
    modelValue: {
      get() {
        return String(this.value).replace('.', ',')
      },
      set(val) {
        const v = parseFloat(String(val).replace(',', '.')) || 0
        this.$emit('input', v)
      },
    },
  },
}
</script>
