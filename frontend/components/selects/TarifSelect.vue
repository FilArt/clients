<template>
  <v-autocomplete
    v-model="tarif"
    :items="tarifs"
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
  computed: mapState({ tarifs: (state) => state.tarifs }),
  watch: {
    value(val) {
      this.tarif = val
    },
  },
  async mounted() {
    if (!this.tarifs.length) {
      this.loading = true
      await this.$store.dispatch('fetchTarifs')
      this.loading = false
    }
  },
}
</script>
