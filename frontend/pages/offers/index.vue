<template>
  <v-card>
    <v-card-title>
      Offers
    </v-card-title>
    <v-card-text>
      <div :class="`d-flex justify-space-around mb-6 flex-wrap`">
        <v-card
          v-for="offer in offers"
          :key="offer.id"
          :to="`offers/${offer.id}`"
          class="pa-1"
          nuxt
          max-width="300"
        >
          <v-img v-if="offer.picture" :src="offer.picture" />
          <v-card-title>
            {{ offer.name }}
          </v-card-title>
        </v-card>
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  data() {
    return {
      offers: []
    }
  },
  mounted() {
    this.refresh()
  },
  methods: {
    refresh() {
      this.$axios.$get('calculator/offers').then(data => (this.offers = data))
    }
  }
}
</script>
