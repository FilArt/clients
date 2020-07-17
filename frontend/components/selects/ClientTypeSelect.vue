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
  >
    <template v-if="hint" v-slot:append-outer>
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn v-on="on" icon color="info" v-bind="attrs">
            <v-icon>
              mdi-information
            </v-icon>
          </v-btn>
        </template>
        <span>
          Elija el perfil de cliente más adecuado para usted.
        </span>
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
    text: 'Negocios',
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
