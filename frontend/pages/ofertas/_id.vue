<template>
  <div>
    <v-card v-for="offer in offers" :key="offer.id" style="margin-bottom: 1em;">
      <detail-offer :offer="offer" />
    </v-card>
  </div>
</template>

<script>
import DetailOffer from '~/components/detailOffer'
export default {
  components: {
    DetailOffer,
  },
  async asyncData({ $axios, query }) {
    let params = {
      name: query.name,
      client_type: query.client_type,
      id: query.id,
    }
    if (query.tarif) {
      params.tarif = query.tarif
    }
    const offers = await $axios.$get('calculator/offers/', { params })
    return { offers }
  },
  data() {
    return {
      isBottomIntersecting: false,
      isTopIntersecting: true,
    }
  },
}
</script>
