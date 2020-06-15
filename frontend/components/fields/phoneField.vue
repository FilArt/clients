<template>
  <v-text-field
    v-model="phone"
    v-mask="'#########'"
    :label="label"
    type="tel"
  />
</template>

<script>
export default {
  name: 'phoneField',
  props: {
    value: {
      type: String,
      default: null,
    },
    label: {
      type: String,
      default: 'Telefono',
    },
  },
  data() {
    return {
      phone: null,
    }
  },
  watch: {
    value: {
      handler: function (val) {
        this.phone = val
      },
      deep: true,
    },
  },
}
</script>
