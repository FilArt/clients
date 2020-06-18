<template>
  <v-text-field
    v-model="email"
    :error-messages="errorMessages"
    label="Email"
    name="email"
    prepend-icon="mdi-at"
    type="email"
  />
</template>

<script>
export default {
  name: 'emailField',
  props: {
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
      handler: function (val) {
        this.email = val
      },
      deep: true,
    },
  },
}
</script>
