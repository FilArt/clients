<template>
  <v-form>
    <company-select v-model="form.company" />
    <tarif-select v-model="form.tarif" all />
    <client-type-select v-model="form.client_type" />
    <decimal-field
      v-for="(decimalField, idx) in decimalFields"
      :key="idx"
      v-model="form[decimalField.value]"
      :label="decimalField.text"
    />
    <offer-select
      v-model="offer"
      :company="form.company"
      :tarif="form.tarif"
      :client-type="form.client_type"
      :p1="form.p1"
      :p2="form.p2"
      :p3="form.p3"
      :p4="form.p4"
      :p5="form.p5"
      :p6="form.p6"
      :consumo="form.consumo"
      @input="$emit('input', offer)"
    />
  </v-form>
</template>
<script>
import constants from '../../lib/constants'
export default {
  name: 'SelectOfferForm',
  components: {
    DecimalField: () => import('@/components/fields/decimalField'),
    CompanySelect: () => import('@/components/selects/CompanySelect'),
    TarifSelect: () => import('@/components/selects/TarifSelect'),
    ClientTypeSelect: () => import('@/components/selects/ClientTypeSelect'),
    OfferSelect: () => import('@/components/selects/OfferSelect'),
  },
  data() {
    return {
      offer: null,
      form: {
        company: null,
        tarif: null,
        client_type: null,
        p1: null,
        p2: null,
        p3: null,
        p4: null,
        p5: null,
        p6: null,
        consumo: null,
      },
    }
  },
  computed: {
    decimalFields() {
      if (!this.form.tarif) return []
      return [
        ...[1, 2, 3, 4, 5, 6]
          .filter((number) => constants.showInput('p', number, this.form.tarif))
          .map((number) => ({ text: `P${number}`, value: `p${number}` })),
        {
          text: 'Consumo',
          value: 'consumo',
        },
      ]
    },
  },
}
</script>
