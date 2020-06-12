<template>
  <v-autocomplete
    v-model="item"
    :items="items"
    label="Typo de cliente"
    chips
    dense
    deletable-chips
    @input="$emit('input', item)"
  />
</template>

<script>
const clientTypes = [
  {
    text: 'Particular',
    value: 0,
  },
  {
    text: 'Negocios',
    value: 1,
  },
]
export default {
  name: 'ClientTypeSelect',
  props: {
    value: {
      type: Number,
      default: -1,
    },
  },
  data() {
    return {
      items: clientTypes,
      item:
        this.value !== -1
          ? clientTypes.find((t) => t.value === this.value)
          : null,
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
