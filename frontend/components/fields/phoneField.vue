<template>
  <v-text-field
    v-model="phone"
    v-mask="'###-###-###'"
    :error-messages="errorMessages"
    :label="label"
    :append-icon="appendIcon"
    name="phone"
    prepend-icon="mdi-phone"
    type="tel"
    @input="$emit('input', $event.split('-').join('') || null)"
    @click:append="$emit('click:append')"
  />
</template>

<script>
export default {
  name: 'phoneField',
  props: {
    appendIcon: {
      type: String,
      default: undefined,
    },
    label: {
      type: String,
      default: 'Teléfono',
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
      phone: this.value,
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
