<template>
  <v-row class="text-center">
    <v-col>
      <v-btn-toggle v-model="item" :color="ourColor" group @change="$emit('input', $event)">
        <v-btn :value="1">PYME</v-btn>
        <v-btn :value="0">RESIDENCIAL</v-btn>
        <v-btn v-if="!withoutAutonomo" :value="2">AUTÓNOMO</v-btn>
      </v-btn-toggle>

      <v-alert v-show="errorMessages" type="error">
        {{ errorMessages.join('\n') }}
      </v-alert>
    </v-col>
  </v-row>
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
    withoutAutonomo: {
      type: Boolean,
      default: false,
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
