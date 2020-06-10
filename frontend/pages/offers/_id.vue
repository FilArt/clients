<template>
  <v-card>
    <v-container>
      <v-row justify="space-between">
        <v-col cols="auto">
          <v-img height="300" width="300" :src="offer.picture" />
        </v-col>
        <v-col>
          <v-card-title>{{ offer.name }}</v-card-title>

          <v-card-text>
            {{ offer.description }}
          </v-card-text>
        </v-col>
      </v-row>
      <v-card-actions>
        <v-row>
          <v-col>
            <v-btn
              :disabled="offer.added"
              rounded
              block
              outlined
              color="success"
              @click="addBid"
            >
              {{ offer.added ? 'Already added' : 'Add to portfel'
              }}<v-icon right>mdi-briefcase</v-icon>
            </v-btn>
          </v-col>
          <v-col>
            <return-button to="/offers" />
          </v-col>
        </v-row>
      </v-card-actions>
    </v-container>
  </v-card>
</template>

<script>
export default {
  components: {
    ReturnButton: () => import('~/components/buttons/returnButton'),
    RefreshButton: () => import('~/components/buttons/refreshButton'),
    CancelButton: () => import('~/components/buttons/cancelButton')
  },
  async asyncData({ $axios, params }) {
    const offer = await $axios.$get(`calculator/offers/${params.id}/`)
    return { offer, id: params.id }
  },
  methods: {
    addBid() {
      if (this.offer.added) return
      this.$axios.$post('bids/', { offer: this.id }).then(() => {
        this.offer.added = true
        this.$swal({
          title: 'Bid added!',
          icon: 'success'
        })
      })
    }
  }
}
</script>
