<template>
  <v-text-field v-model="email" :label="label" type="email" />
</template>

<script>
export default {
  name: 'emailField',
  props: {
    value: {
      type: String,
      default: null,
    },
    label: {
      type: String,
      default: 'Email',
    },
  },
  data() {
    return {
      email: null,
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
