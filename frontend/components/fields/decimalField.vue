<template>
  <div>
    <v-text-field v-model="modelValue" :label="label" :errors-messages="errorMessages" />
  </div>
</template>

<script>
export default {
  name: 'DecimalField',
  props: {
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
