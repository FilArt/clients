<template>
  <v-autocomplete
    v-model="item"
    :items="statuses"
    :multiple="multiple"
    label="Estados"
    style="min-width: 150px;"
    chips
    dense
    deletable-chips
    @input="$emit('input', status)"
  />
</template>

<script>
export default {
  name: 'StatusSelect',
  props: {
    value: {
      type: String,
      default: '',
    },
    multiple: {
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
