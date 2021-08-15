<template>
  <v-form>
    <v-card-text class="text-center">
      <v-btn-toggle v-model="form.client_type">
        <v-btn :value="0">Residencial - Físico</v-btn>
        <v-btn :value="1">Jurídico (empresa)</v-btn>
        <v-btn :value="2">PYME - Físico (autonomo)</v-btn>
      </v-btn-toggle>
    </v-card-text>

    <v-card-text class="text-center">
      <v-btn-toggle v-model="form.kind" mandatory>
        <v-btn value="luz">
          Luz
          <v-icon color="warning" right>mdi-flash</v-icon>
        </v-btn>
        <v-btn value="gas">
          Gas
          <v-icon color="blue" right>mdi-fire</v-icon>
        </v-btn>
      </v-btn-toggle>
    </v-card-text>
    <company-select v-model="form.company" />
    <tarif-select v-model="form.tarif" all />
    <decimal-field
      v-for="(decimalField, idx) in decimalFields"
      :key="idx"
      v-model="form[decimalField.value]"
      :label="decimalField.text"
    />
    <offer-select
      v-model="offer"
      :company="form.company"
      :kind="form.kind"
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
export default {
  name: 'SelectOfferForm',
  components: {
    DecimalField: () => import('@/components/fields/decimalField'),
    CompanySelect: () => import('@/components/selects/CompanySelect'),
    TarifSelect: () => import('@/components/selects/TarifSelect'),
    OfferSelect: () => import('@/components/selects/OfferSelect'),
  },
  data() {
    return {
      offer: null,
      form: {
        kind: null,
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
          .filter((number) => (this.form.tarif === '2.0TD' ? [1, 2].includes(number) : true))
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
