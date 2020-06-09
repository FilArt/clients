<template>
  <v-dialog v-model="dialog">
    <template v-slot:activator="{ on }">
      <v-btn icon v-on="on" @click="fetchCard">
        <v-icon>mdi-details-card</v-icon>
      </v-btn>
    </template>
    <client-card :card="fetchedCard" />
  </v-dialog>
</template>

<script>
export default {
  name: 'ClientCardDialog',
  components: { ClientCard: () => import('~/components/card/ClientCard') },
  props: {
    cardId: {
      type: Number,
      default: 0
    },
    card: {
      type: Object,
      default: () => null
    }
  },
  data() {
    return {
      dialog: false,
      loadedCard: null
    }
  },
  computed: {
    fetchedCard() {
      return this.card ? this.card : this.loadedCard
    }
  },
  methods: {
    async fetchCard() {
      this.$http
        .$get(`/cards/${this.cardId}/`)
        .then(data => (this.loadedCard = data))
    }
  }
}
</script>
