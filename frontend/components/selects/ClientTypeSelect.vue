<template>
  <v-btn-toggle v-model="item" :error-messages="errorMessages" :color="ourColor" @change="$emit('input', $event)">
    <v-btn :value="0">RESIDENCIAL</v-btn>
    <v-btn :value="1">PYME</v-btn>
    <v-btn :value="2">AUTÓNOMO</v-btn>
  </v-btn-toggle>
</template>

<script>
import constants from '@/lib/constants'

export default {
  name: 'ClientTypeSelect',
  props: {
    value: {
      type: Number,
      default: 0,
    },
    errorMessages: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      ourColor: constants.ourColor,
      item: this.value,
    }
  },
  watch: {
    value(val) {
      this.item = val
    },
  },
}
</script>
