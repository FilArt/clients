<template>
  <v-row justify="center">
    <v-col v-for="offer in offers" :key="offer.id" xl="6" lg="8" md="12">
      <v-sheet>
        <detail-offer :offer="offer" show-add-btn />
      </v-sheet>
    </v-col>
  </v-row>
</template>

<script>
import DetailOffer from '~/components/detailOffer'

export default {
  auth: false,
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
