<template>
  <v-container>
    <v-toolbar>
      <v-toolbar-title> Ofertas (totales: {{ total }}) </v-toolbar-title>
      <v-spacer />
      <v-toolbar-items class="pa-1">
        <v-container>
          <client-type-select
            :value="clientTypeShortcuts[$route.query.client_type]"
            @input="updateFilters('client_type', $event)"
          />
        </v-container>
        <v-container>
          <tarif-select
            :value="filters.tarif"
            @input="updateFilters('tarif', $event)"
          />
        </v-container>
      </v-toolbar-items>
    </v-toolbar>
    <v-card-text>
      <v-responsive class="overflow-y-auto">
        <v-row class="d-flex align-center justify-space-around flex-wrap">
          <v-col v-for="offer in offers" :key="offer.id">
            <v-card
              :to="`/offers/${offer.id}?tarif=${
                filters.tarif || ''
              }&client_type=${filters.client_type}`"
              nuxt
              class="mx-auto"
              max-width="300"
            >
              <v-img :src="offer.picture || '/no-image.svg'" />
              <v-card-subtitle
                v-text="offer.company + ' (id:' + offer.id + ')'"
              />
              <v-card-title>{{ offer.name }} </v-card-title>
            </v-card>
          </v-col>

          <v-card
            class="mx-auto"
            max-width="336"
            v-intersect="{
              handler: onIntersect,
              options: {
                threshold: [0, 0.5, 1.0],
              },
            }"
            >loaded: {{ offers.length }}</v-card
          >
        </v-row>
      </v-responsive>
    </v-card-text>

    <v-btn
      fab
      x-large
      icon
      large
      fixed
      bottom
      right
      color="yellow"
      @click="$vuetify.goTo(0)"
    >
      <v-icon>mdi-arrow-up</v-icon>
    </v-btn>
  </v-container>
</template>

<script>
const baseUrl = 'calculator/offers/'
const clientTypeShortcuts = {
  0: 'individual',
  individual: 0,
  1: 'business',
  business: 1,
}
export default {
  components: {
    TarifSelect: () => import('~/components/selects/TarifSelect'),
    ClientTypeSelect: () => import('~/components/selects/ClientTypeSelect'),
  },
  data() {
    return {
      clientTypeShortcuts,
      offers: [],
      nextUrl: this.$route.query.client_type
        ? baseUrl +
          `?client_type=${clientTypeShortcuts[this.$route.query.client_type]}`
        : baseUrl,
      total: 0,
      loading: false,
      filters: {
        tarif: undefined,
        client_type: clientTypeShortcuts[this.$route.query.client_type],
      },
    }
  },
  methods: {
    updateFilters(key, value) {
      console.log(this.filters.client_type)
      if (!value && key !== 'client_type' && value !== 0) return
      this.filters[key] = value

      let nextUrl = baseUrl + '?' + key + '=' + value

      if (key === 'tarif') {
        nextUrl = nextUrl + '&client_type=' + this.filters.client_type
      } else {
        nextUrl = nextUrl + '&tarif=' + (this.filters.tarif || '')
      }
      this.offers = []
      this.nextUrl = nextUrl
      this.fetch()
    },
    async fetch() {
      if (this.loading === true || !this.nextUrl) return
      this.loading = true
      const data = await this.$axios.$get(this.nextUrl)

      this.offers = [...(this.offers || []), ...data.results]
      this.nextUrl = data.next
      this.total = data.count
      this.loading = false
    },
    async onIntersect() {
      await this.fetch()
    },
  },
}
</script>
