<template>
  <v-card>
    <v-card-text>
      <offers-list-toolbar
        :total="offers.length"
        :default-filters="filters"
        @filters-updated="
          filters = $event
          fetch()
        "
      />
    </v-card-text>
    <v-card-text>
      <offers-list :offers="offers" />
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
  name: 'OffersView',
  components: {
    OffersListToolbar: () => import('~/components/offers/OffersListToolbar'),
    OffersList: () => import('~/components/offers/OffersList'),
    GoUpButton: () => import('~/components/buttons/goUpButton'),
  },
  props: {
    defaultFilters: {
      type: Object,
      default: () => {},
    },
  },
  data() {
    return {
      loading: false,
      offers: [],
      filters: this.defaultFilters,
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
    async fetch() {
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
