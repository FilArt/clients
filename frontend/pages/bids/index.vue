<template>
  <v-container>
    <v-progress-circular v-if="loading" indeterminate />
    <v-alert v-else-if="!loading && bids.length === 0">
      No bids so far.
    </v-alert>
    <v-list v-else>
      <v-list-item
        :key="bid.id"
        v-for="bid in bids"
        nuxt
        :to="`bids/${bid.id}`"
      >
        <v-list-item-subtitle>{{ bid.id }}</v-list-item-subtitle>
        <v-list-item-title>
          {{ $dateFns.format(bid.created_at, 'dd/MM/yyyy') }}
        </v-list-item-title>
      </v-list-item>
    </v-list>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      loading: false,

      bids: []
    }
  },
  mounted() {
    this.refresh()
  },
  methods: {
    refresh() {
      this.loading = true
      this.$axios
        .$get('bids/')
        .then(data => (this.bids = data))
        .finally(() => (this.loading = false))
    }
  }
}
</script>
