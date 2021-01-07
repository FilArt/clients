<template>
  <v-select
    :label="label"
    :items="$store.state.cvusers.filter((u) => u.position === type)"
    item-text="fullname"
    item-value="id"
    @input="$emit('input', $event)"
  />
</template>

<script>
const names = new Map([
  ['manager', 'Agentes'],
  ['operator', 'Teleoperadores'],
  ['tele', 'Teleconcentadores'],
])
export default {
  name: 'CvUserSelect',
  props: {
    type: {
      type: String,
      default: 'manager',
    },
  },
  computed: {
    label() {
      return names.get(this.type)
    },
  },
}
</script>
