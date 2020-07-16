<template>
  <v-col>
    <v-card v-for="offer in offers" :key="offer.id" style="margin-bottom: 1em;">
      <detail-offer
        :offer="offer"
        :show-actions="!$route.query.showCalculatorDetails"
      />
      <calculator-details
        v-if="$route.query.showCalculatorDetails"
        :offer="offer"
      />
    </v-card>
  </v-col>
</template>

<script>
import DetailOffer from '~/components/detailOffer'
const filterFields = [
  'id',
  'company',
  'company_logo',
  'c1',
  'c2',
  'c3',
  'p1',
  'p2',
  'p3',
  'tarif',
  'description',
  'name',
  'power_min',
  'power_max',
  'consumption_min',
  'consumption_max',
  'client_type',
].join(',')
export default {
  components: {
    DetailOffer,
    CalculatorDetails: () => import('~/components/CalculatorDetails'),
    returnButton: () => import('~/components/buttons/returnButton'),
  },
  data() {
    return {
      isBottomIntersecting: false,
      isTopIntersecting: true,
    }
  },
  async asyncData({ $axios, query }) {
    let params = {
      name: query.name,
      client_type: query.client_type,
      fields: filterFields,
      id: query.id,
    }
    const offers = await $axios.$get('calculator/offers/', { params })
    return { offers }
  },
}
</script>
