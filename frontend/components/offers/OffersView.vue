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
      <offers-list :offers="offers" :filters="filters" />
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'OffersView',
  components: {
    OffersListToolbar: () => import('~/components/offers/OffersListToolbar'),
    OffersList: () => import('~/components/offers/OffersList'),
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
  watch: {
    filters: {
      handler(v) {
        this.$router.replace({ query: v })
      },
      deep: true,
    },
  },
  async mounted() {
    await this.fetch()
  },
  methods: {
    async fetch() {
      this.loading = true
      try {
        this.offers = await this.$axios.$get('calculator/offers/', {
          params: { ...this.filters },
        })
      } catch (e) {
        const errData = e.response.data
        this.$swal({
          title: 'Error',
          icon: 'error',
          text: Object.keys(errData)
            .map((key) => `${key}: ${errData[key].join(', ')}`)
            .join('\n'),
        })
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
