<template>
  <v-row>
    <v-col v-for="offer in offers" :key="offer.id" cols="12">
      <detail-offer :offer="offer" show-add-btn />
    </v-col>
  </v-row>
</template>

<script>
import DetailOffer from '~/components/detailOffer'

export default {
  components: {
    DetailOffer,
  },
  async asyncData({ $axios, query }) {
    const params = {
      name: query.name,
      client_type: 0,
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
