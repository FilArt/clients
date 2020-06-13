<template>
  <v-card>
    <v-card-title> Bid {{ $route.params.id }} </v-card-title>
    <v-card-text>
      <v-list>
        <v-list-item v-for="(value, name) in bid" :key="name">
          <v-list-item-group v-if="typeof value === 'object'">
            <v-list-item-title>{{ name }}</v-list-item-title>
            <v-list-item v-for="(v1, n1) in value" :key="n1" class="text-right">
              <v-list-item-title>{{ n1 }}: {{ v1 }}</v-list-item-title>
            </v-list-item>
          </v-list-item-group>

          <v-list-item-title v-else>{{ name }}: {{ value }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-card-text>
    <v-card-actions>
      <delete-button @click="deleteBid" />
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  components: {
    DeleteButton: () => import('~/components/buttons/deleteButton'),
  },
  async asyncData({ $axios, params }) {
    const bid = await $axios.$get(`bids/${params.id}`)
    return { bid, id: params.id }
  },
  methods: {
    deleteBid() {
      const bidId = this.bid.id
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
          this.$router.push('/bids')
        }
      })
    },
  },
}
</script>
