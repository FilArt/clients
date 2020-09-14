<template>
  <v-autocomplete
    v-model="item"
    :items="statuses"
    :error-messages="errors"
    label="Estado"
    style="min-width: 150px"
    :return-object="returnObject"
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
    all: {
      type: Boolean,
      default: false,
    },
    errors: {
      type: Array,
      default: () => [],
    },
    value: {
      type: String,
      default: '',
    },
    returnObject: {
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
  watch: {
    value: {
      handler(val) {
        this.item = val
      },
      deep: true,
    },
  },
  async mounted() {
    const aep = 'bids/bids/statuses/'
    this.statuses = await this.$axios.$get(this.all ? `${aep}?all=true` : aep)
  },
}
</script>
