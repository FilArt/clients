<template>
  <v-responsive class="overflow-y-auto">
    <v-row class="d-flex align-center justify-space-around flex-wrap">
      <v-col v-for="offer in offers" :key="offer.id">
        <v-card
          :to="detailOfferUrl(offer)"
          nuxt
          class="mx-auto"
          max-width="300"
        >
          <v-img :src="offer.company_logo || '/no-image.svg'" />
          <v-card-subtitle v-text="'Comercializadora: ' + offer.company" />
          <v-card-text>{{ offer.name }}</v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-responsive>
</template>
<script>
export default {
  name: 'OffersList',
  props: {
    offers: {
      type: Array,
      default: () => [],
    },
    tarif: {
      type: String,
      default: '',
    },
  },
  methods: {
    detailOfferUrl(offer) {
      let params = {
        name: offer.name,
        is_price_permanent: offer.is_price_permanent,
      }
      if (this.tarif) {
        params.tarif = this.tarif
      }
      const query = Object.keys(params)
        .map((k) => encodeURIComponent(k) + '=' + encodeURIComponent(params[k]))
        .join('&')

      return `/ofertas/${offer.id}/?${query}`
    },
  },
}
</script>
