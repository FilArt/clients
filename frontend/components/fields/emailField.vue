<template>
  <v-text-field
    v-model="email"
    :error-messages="errorMessages"
    :label="label"
    name="email"
    prepend-icon="mdi-at"
    type="email"
    @input="$emit('input', $event)"
  />
</template>

<script>
export default {
  name: 'EmailField',
  props: {
    label: {
      type: String,
      default: 'Email',
    },
    value: {
      type: String,
      default: null,
    },
    errorMessages: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      email: this.value,
    }
  },
  watch: {
    value: {
      handler(val) {
        this.email = val
      },
      deep: true,
    },
  },
}
</script>
