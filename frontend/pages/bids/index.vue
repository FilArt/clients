<template>
  <v-container>
    <v-alert v-if="bids.length === 0">
      No bids so far.
    </v-alert>
    <v-list v-else nav>
      <v-list-item
        :key="bid.id"
        v-for="bid in bids"
        :to="`bids/${bid.id}`"
        link
      >
        <v-list-item-content>
          <v-list-item-subtitle>{{ bid.id }}</v-list-item-subtitle>
          <v-list-item-title>
            {{ $dateFns.format(bid.created_at, 'dd/MM/yyyy') }}
          </v-list-item-title>
        </v-list-item-content>
        <v-list-item-action @click.prevent="deleteBid(bid.id)">
          <delete-button />
        </v-list-item-action>
      </v-list-item>
    </v-list>
  </v-container>
</template>

<script>
export default {
  components: {
    DeleteButton: () => import('~/components/buttons/deleteButton'),
  },
  async asyncData({ $axios }) {
    const data = await $axios.$get('bids/')
    return { bids: data }
  },
  methods: {
    deleteBid(bidId) {
      this.$swal({
        title: `Delete bid ${bidId}?`,
        text: 'Once deleted, you will not be able to recover this bid!',
        icon: 'warning',
        buttons: true,
        dangerMode: true,
      }).then((willDelete) => {
        if (willDelete) {
          this.$axios.$delete(`bids/${bidId}/`).then(() => {
            this.bids = this.bids.filter((bid) => bid.id !== bidId)
            this.$swal({ title: 'Solicitud eliminada!', icon: 'success' })
          })
        }
      })
    },
  },
}
</script>
