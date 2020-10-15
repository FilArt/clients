<template>
  <v-autocomplete
    v-model="tarif"
    :items="gas ? tarifsGas : tarifs"
    :loading="loading"
    :error-messages="errorMessages"
    label="Tarifa"
    style="min-width: 50px"
    chips
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
import { mapState } from 'vuex'
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
      loading: false,
      tarif: this.value,
    }
  },
  computed: mapState({ tarifs: (state) => state.tarifs, tarifsGas: (state) => state.tarifsGas }),
  watch: {
    value(val) {
      this.tarif = val
    },
    gas() {
      this.refresh()
    },
  },
  async mounted() {
    this.loading = true
    await this.refresh()
    this.loading = false
  },
  methods: {
    async refresh() {
      this.gas ? await this.$store.dispatch('fetchTarifsGas') : await this.$store.dispatch('fetchTarifs')
    },
  },
}
</script>
