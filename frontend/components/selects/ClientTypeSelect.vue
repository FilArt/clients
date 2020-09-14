<template>
  <v-autocomplete
    v-model="item"
    :items="items"
    :error-messages="errorMessages"
    label="Tipo de cliente"
    style="min-width: 150px"
    chips
    deletable-chips
    @input="$emit('input', item)"
  >
    <template v-if="hint" v-slot:append-outer>
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon color="#004680" v-bind="attrs" v-on="on">
            <v-icon> mdi-information </v-icon>
          </v-btn>
        </template>
        <span> Elija el perfil de cliente más adecuado para usted. </span>
      </v-tooltip>
    </template>
  </v-autocomplete>
</template>

<script>
const clientTypes = [
  {
    text: 'Particular',
    value: '0',
  },
  {
    text: 'Juridico',
    value: '1',
  },
]
export default {
  name: 'ClientTypeSelect',
  props: {
    hint: {
      type: Boolean,
      default: false,
    },
    value: {
      type: String,
      default: '',
    },
    errorMessages: {
      type: Array,
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
      handler(val) {
        this.item = this.items.find((i) => i.value === val)
      },
      deep: true,
    },
  },
}
</script>
