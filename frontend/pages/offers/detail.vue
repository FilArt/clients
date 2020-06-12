<template>
  <v-container>
    <v-card-text>
      <v-card-title>Ofertas (totales: {{ offers.length }})</v-card-title>
      <v-card-text>
        <v-row align="center">
          <v-col>
            <client-type-select v-model="filters.client_type" @input="fetch" />
          </v-col>
          <v-col>
            <company-select v-model="filters.company" @input="fetch" />
          </v-col>
          <v-col>
            <tarif-select v-model="filters.tarif" @input="fetch" />
          </v-col>
        </v-row>
      </v-card-text>
    </v-card-text>
    <v-card-text>
      <v-responsive class="overflow-y-auto">
        <v-row class="d-flex align-center justify-space-around flex-wrap">
          <v-col v-for="offer in offers" :key="offer.id">
            <v-card
              :to="`/offers/${offer.id}?back=${$route.fullPath.replaceAll(
                '&',
                '@'
              )}`"
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
export default {
  components: {
    CompanySelect: () => import('~/components/selects/CompanySelect'),
    TarifSelect: () => import('~/components/selects/TarifSelect'),
    ClientTypeSelect: () => import('~/components/selects/ClientTypeSelect'),
  },
  data() {
    return {
      offers: [],
      loading: false,
      filters: {
        fields: 'id,name,picture,company',
        company: this.$route.query.company
          ? parseInt(this.$route.query.company)
          : null,
        tarif: this.$route.query.tarif || '',
        client_type: this.$route.query.client_type,
      },
    }
  },
  watch: {
    filters: {
      handler: function (v) {
        this.$router.replace({ query: v })
      },
      deep: true,
    },
  },
  methods: {
    async fetch() {
      if (this.loading === true) return
      this.loading = true
      try {
        this.offers = await this.$axios.$get('calculator/offers/', {
          params: this.filters,
        })
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
