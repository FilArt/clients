<template>
  <v-autocomplete
    v-model="item"
    :items="items"
    label="Typo de cliente"
    @input="$emit('input', item)"
  />
</template>

<script>
export default {
  name: 'ClientTypeSelect',
  data() {
    return {
      item: 0,
      items: [
        {
          text: 'Particular',
          value: 0
        },
        {
          text: 'Negocios',
          value: 1
        }
      ]
    }
  }
}
</script>
