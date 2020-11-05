<template>
  <v-autocomplete
    v-model="tarif"
    :items="gas ? tarifsGas : tarifs"
    :error-messages="errorMessages"
    label="Tarifa"
    style="min-width: 50px"
    chips
    dense
    deletable-chips
    @input="$emit('input', tarif)"
  >
    <template v-if="hint" v-slot:append-outer>
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon color="#004680" v-bind="attrs" v-on="on">
            <v-icon> mdi-information </v-icon>
          </v-btn>
        </template>

        <span> Elija su tarifa o peaje de acceso. Está información puede obtenerse en su factura. </span>
      </v-tooltip>
    </template>
  </v-autocomplete>
</template>

<script>
import constants from '@/lib/constants'

export default {
  name: 'TarifSelect',
  props: {
    gas: {
      type: Boolean,
      default: false,
    },
    hint: {
      type: Boolean,
      default: false,
    },
    value: {
      type: String,
      default: null,
    },
    errorMessages: {
      type: Array,
      default: () => null,
    },
  },
  data() {
    return {
      tarif: this.value,
      tarifs: constants.tarifs,
      tarifsGas: constants.tarifsGas,
    }
  },
  watch: {
    value(val) {
      this.tarif = val
    },
  },
}
</script>
