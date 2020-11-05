<template>
  <v-card-text>
    {{ label }}
    <v-row align="center">
      <v-col>
        <company-select v-model="company" />
      </v-col>
      <v-col>
        <tarif-select v-model="tarif" :gas="newOffer && newOffer.kind === 'gas'" />
      </v-col>
      <v-col>
        <client-type-select v-model="clientType" />
      </v-col>
      <v-col v-if="company && tarif">
        <offer-select
          v-model="newOffer"
          :company="company"
          :tarif="tarif"
          :client-type="clientType"
          @input="$emit('input', newOffer)"
        />
      </v-col>
    </v-row>
  </v-card-text>
</template>

<script>
import CompanySelect from '@/components/selects/CompanySelect'
import TarifSelect from '@/components/selects/TarifSelect'
import ClientTypeSelect from '@/components/selects/ClientTypeSelect'
import OfferSelect from '@/components/selects/OfferSelect'
export default {
  name: 'SelectOffer',
  components: { OfferSelect, ClientTypeSelect, TarifSelect, CompanySelect },
  props: {
    label: {
      type: String,
      default: 'Editar oferta',
    },
  },
  data() {
    return {
      newOffer: null,
      company: null,
      tarif: null,
      clientType: null,
    }
  },
}
</script>
