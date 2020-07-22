<template>
  <v-card>
    <v-card-text>
      <v-card-title>Ofertas (totales: {{ offers.length }})</v-card-title>
      <v-card-text>
        <v-row align="center">
          <v-col>
            <v-select
              v-model="filters.is_price_permanent"
              label="Typo de precio"
              :items="[
                {
                  text: 'FIJO',
                  value: true,
                },
                {
                  text: 'INDEXADO',
                  value: false,
                },
              ]"
              @input="fetch"
            />
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
              :to="`/offers/detail/${offer.id}?name=${myEscape(
                offer.name
              )}&is_price_permanent=${offer.is_price_permanent}&tarif=${
                filters.tarif || ''
              }`"
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
    </v-card-text>

    <go-up-button style="margin-bottom: 5rem; margin-right: 5px;" />
  </v-card>
</template>

<script>
const filterFields = [
  'id',
  'company',
  'company_logo',
  'name',
  'is_price_permanent',
].join(',')
export default {
  components: {
    GoUpButton: () => import('~/components/buttons/goUpButton'),
    CompanySelect: () => import('~/components/selects/CompanySelect'),
    TarifSelect: () => import('~/components/selects/TarifSelect'),
    ClientTypeSelect: () => import('~/components/selects/ClientTypeSelect'),
  },
  data() {
    return {
      loading: false,
      offers: [],
      filters: {
        company: this.$route.query.company
          ? parseInt(this.$route.query.company || '1')
          : '',
        tarif: this.$route.query.tarif,
        is_price_permanent: this.$route.query.is_price_permanent,
      },
    }
  },
  async mounted() {
    await this.fetch()
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
    myEscape(some) {
      return window.escape(some).trim()
    },
    async fetch() {
      if (this.loading === true) return
      this.loading = true
      try {
        this.offers = await this.$axios.$get('calculator/offers/', {
          params: { ...this.filters, fields: filterFields },
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
  },
}
</script>
