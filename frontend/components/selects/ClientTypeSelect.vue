<template>
  <v-autocomplete
    v-model="item"
    :items="items"
    :error-messages="errorMessages"
    label="Typo de cliente"
    style="min-width: 150px;"
    chips
    deletable-chips
    @input="$emit('input', item)"
  />
</template>

<script>
const clientTypes = [
  {
    text: 'Particular',
    value: '0',
  },
  {
    text: 'Negocios',
    value: '1',
  },
]
export default {
  name: 'ClientTypeSelect',
  props: {
    value: {
      type: String,
      default: '',
    },
    errorMessages: {
      value: Array,
      default: () => [],
    },
  },
  data() {
    return {
      items: clientTypes,
      item: clientTypes.find((t) => t.value === this.value),
    }
  },
  watch: {
    value: {
      handler: function (val) {
        this.item = this.items.find((i) => i.value === val)
      },
      deep: true,
    },
  },
}
</script>
