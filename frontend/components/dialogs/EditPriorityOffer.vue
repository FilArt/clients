<template>
  <v-dialog v-model="createOfferDialog">
    <template v-slot:activator="{ on }">
      <v-btn v-if="updating" color="info" icon v-on="on"><v-icon>mdi-pencil</v-icon></v-btn>
      <v-btn v-else icon color="success" v-on="on"><v-icon>mdi-plus</v-icon></v-btn>
    </template>
    <v-form @submit.prevent="createOffer">
      <v-card>
        <v-card-title>Anadir prioridad de ofertas</v-card-title>
        <v-card-text>
          <v-select
            v-model="newOffer.kind"
            :items="['luz', 'gas']"
            label="Tipo"
            :error-messages="newOfferErrors.kind"
          />
          <tarif-select v-model="newOffer.tarif" :error-messages="newOfferErrors.tarif" />
          <decimal-field
            v-model="newOffer.consumption_min"
            label="Consumo min"
            :error-messages="newOfferErrors.consumption_min"
          />
          <decimal-field
            v-model="newOffer.consumption_max"
            label="Consumo max"
            :error-messages="newOfferErrors.consumption_max"
          />
          <decimal-field
            v-model="newOffer.power_min"
            label="Potencia min"
            :error-messages="newOfferErrors.consumption_min"
          />
          <decimal-field
            v-model="newOffer.power_max"
            label="Potencia max"
            :error-messages="newOfferErrors.consumption_max"
          />

          <offer-select
            v-model="newOffer.first"
            label="Primero"
            :return-object="false"
            :kind="newOffer.kind || offer.kind"
            :tarif="newOffer.tarif || offer.tarif"
            :error-messages="newOfferErrors.first"
            :default-items="updating ? [{ id: newOffer.first, name: newOffer.first_name }] : []"
          />
          <offer-select
            v-model="newOffer.second"
            label="Segundo"
            :return-object="false"
            :kind="newOffer.kind || offer.kind"
            :tarif="newOffer.tarif || offer.tarif"
            :error-messages="newOfferErrors.second"
            :default-items="updating ? [{ id: newOffer.second, name: newOffer.second_name }] : []"
          />
          <offer-select
            v-model="newOffer.third"
            label="Tercero"
            :return-object="false"
            :kind="newOffer.kind || offer.kind"
            :tarif="newOffer.tarif || offer.tarif"
            :error-messages="newOfferErrors.third"
            :default-items="updating ? [{ id: newOffer.third, name: newOffer.third_name }] : []"
          />
        </v-card-text>

        <v-card-actions>
          <close-button @click="createOfferDialog = false" />
          <submit-button />
        </v-card-actions>
      </v-card>
    </v-form>
  </v-dialog>
</template>

<script>
import CloseButton from '@/components/buttons/closeButton.vue'
import submitButton from '@/components/buttons/submitButton.vue'
import DecimalField from '@/components/fields/decimalField.vue'
import TarifSelect from '@/components/selects/TarifSelect.vue'
import OfferSelect from '@/components/selects/OfferSelect.vue'

const defaultNewOffer = {
  kind: 'luz',
  tarif: null,
  consumption_min: null,
  consumption_max: null,
  power_min: null,
  power_max: null,
  first: null,
  second: null,
  third: null,
}
export default {
  name: 'EditPriorityOffer',
  components: { submitButton, CloseButton, TarifSelect, DecimalField, OfferSelect },
  props: {
    updating: {
      type: Boolean,
      default: false,
    },
    offer: {
      type: Object,
      default: () => defaultNewOffer,
    },
  },
  data() {
    return {
      newOffer: this.offer,
      createOfferDialog: false,
      newOfferErrors: {},
    }
  },
  methods: {
    async createOffer() {
      this.newOfferErrors = {}
      try {
        const method = this.updating ? this.$axios.$patch : this.$axios.$post
        const url = this.updating ? `calculator/priority_offers/${this.offer.id}/` : 'calculator/priority_offers/'
        await method(url, { ...this.newOffer })
        this.$toast.global.done()
        this.createOfferDialog = false
        this.$emit('update')
      } catch (e) {
        this.newOfferErrors = e.response.data
      }
    },
  },
}
</script>
