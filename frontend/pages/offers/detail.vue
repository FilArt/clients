<template>
  <v-container>
    <v-card-text>
      <v-card-title>Ofertas (totales: {{ total }})</v-card-title>
      <v-card-text>
        <v-row align="center">
          <v-col>
            <client-type-select v-model="filters.client_type" />
          </v-col>
          <v-col>
            <company-select v-model="filters.company" />
          </v-col>
          <v-col>
            <tarif-select v-model="filters.tarif" />
          </v-col>
        </v-row>
      </v-card-text>
    </v-card-text>
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
export default {
  components: {
    CompanySelect: () => import('~/components/selects/CompanySelect'),
    TarifSelect: () => import('~/components/selects/TarifSelect'),
    ClientTypeSelect: () => import('~/components/selects/ClientTypeSelect'),
  },
  data() {
    return {
      offers: [],
      nextUrl: this.getNextUrl(),
      total: 0,
      loading: false,
      filters: {
        company: this.$route.query.company
          ? parseInt(this.$route.query.company)
          : null,
        tarif: this.$route.query.tarif || '',
        client_type: parseInt(this.$route.query.client_type || '0'),
      },
    }
  },
  watch: {
    filters: {
      handler: async function (v) {
        this.offers = []
        this.nextUrl =
          baseUrl +
          `?client_type=${v.client_type || ''}&tarif=${v.tarif || ''}&company=${
            v.company || ''
          }`
        await this.$router.replace({ query: v })
        await this.fetch()
      },
      deep: true,
    },
  },
  methods: {
    getNextUrl() {
      return this.$route.query.client_type
        ? baseUrl +
            `?client_type=${this.$route.query.client_type}&tarif=${
              this.$route.query.tarif || ''
            }`
        : baseUrl
    },
    async fetch() {
      if (this.loading === true || !this.nextUrl) return
      this.loading = true
      try {
        const data = await this.$axios.$get(this.nextUrl)
        this.offers = [...(this.offers || []), ...data.results]
        this.nextUrl = data.next
        this.total = data.count
      } catch (e) {
        const errData = e.response.data
        this.$swal({
          title: 'Error',
          icon: 'error',
          text: Object.keys(errData)
            .map((key) => key + ': ' + errData[key].join(', '))
            .join('\n'),
        })
      } finally {
        this.loading = false
      }
    },
    async onIntersect() {
      await this.fetch()
    },
  },
}
</script>
