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
      tarifs: ['2.0A', '2.1A', '2.0DHA', '2.0DHS', '2.1DHA', '2.1DHS', '3.0A', '3.1A'],
      tarifsGas: ['3.1', '3.2', '3.3', '3.4'],
    }
  },
  watch: {
    value(val) {
      this.tarif = val
    },
  },
}
</script>
