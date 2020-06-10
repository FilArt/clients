<template>
  <v-card>
    <v-card-title> Bid {{ $route.params.id }} </v-card-title>
    <v-card-text>
      {{ bid }}
    </v-card-text>
    <v-card-actions>
      <return-button to="/bids" />
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  components: {
    ReturnButton: () => import('~/components/buttons/returnButton')
  },
  async asyncData({ $axios, params }) {
    const bid = await $axios.$get(`bids/${params.id}`)
    return { bid, id: params.id }
  }
}
</script>
