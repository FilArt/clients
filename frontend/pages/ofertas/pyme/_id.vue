<template>
  <v-row>
    <v-col v-for="offer in offers" :key="offer.id" xl="4" lg="6" md="12">
      <v-sheet>
        <detail-offer :offer="offer" show-add-btn />
      </v-sheet>
    </v-col>
  </v-row>
</template>

<script>
import DetailOffer from '~/components/detailOffer'

export default {
  auth: 'guest',
  components: {
    DetailOffer,
  },
  async asyncData({ $axios, query }) {
    const params = {
      name: query.name,
      client_type: 1,
      id: query.id,
    }
    if (query.tarif) {
      params.tarif = query.tarif
    }
    const offers = await $axios.$get('calculator/offers/', { params })
    return { offers }
  },
}
</script>
