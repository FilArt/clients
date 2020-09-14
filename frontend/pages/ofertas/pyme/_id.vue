<template>
  <div>
    <detail-offer v-for="offer in offers" :key="offer.id" :offer="offer" show-add-btn />
  </div>
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
