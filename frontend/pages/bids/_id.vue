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
import ReturnButton from '~/components/buttons/returnButton'
export default {
  components: { ReturnButton },
  data() {
    return {
      bid: null,
      id: this.$route.params.id
    }
  },
  mounted() {
    this.refresh()
  },
  methods: {
    async refresh() {
      this.$axios.$get(`bids/${this.id}`).then(data => (this.bid = data))
    }
  }
}
</script>
