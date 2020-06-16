<template>
  <v-autocomplete
    v-model="item"
    :items="statuses"
    :multiple="multiple"
    :label="multiple ? 'Estados' : 'Estado'"
    :error-messages="errors"
    style="min-width: 150px;"
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
    multiple: {
      type: Boolean,
      default: false,
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
