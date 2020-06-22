<template>
  <v-autocomplete
    v-model="item"
    :items="statuses"
    :error-messages="errors"
    label="Estado"
    style="min-width: 150px;"
    return-object
    chips
    dense
    deletable-chips
    @input="$emit('input', item)"
  />
</template>

<script>
export default {
  name: 'StatusSelect',
  props: {
    errors: {
      type: Array,
      default: () => [],
    },
    value: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      item: this.value,
      statuses: [],
    }
  },
  async mounted() {
    this.statuses = await this.$axios.$get('bids/statuses/')
  },
  watch: {
    value: {
      handler: function (val) {
        this.item = val
      },
      deep: true,
    },
  },
}
</script>
