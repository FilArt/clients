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
              }}<v-icon>mdi-briefcase</v-icon>
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
import CancelButton from '~/components/buttons/cancelButton'
import RefreshButton from '~/components/buttons/refreshButton'
import ReturnButton from '~/components/buttons/returnButton'
export default {
  components: { ReturnButton, RefreshButton, CancelButton },
  data() {
    return {
      loading: false,
      offer: {},
      id: this.$route.params.id
    }
  },
  mounted() {
    this.refresh()
  },
  methods: {
    refresh() {
      this.loading = true
      this.$axios
        .$get(`calculator/offers/${this.$route.params.id}/`)
        .then(data => (this.offer = data))
        .finally(() => (this.loading = false))
    },
    addBid() {
      if (this.offer.added) return
      this.$axios.$post('bids', { offer: this.id }).then(() => {
        this.$swal({
          title: 'Bid added!',
          icon: 'success'
        })
      })
    }
  }
}
</script>
