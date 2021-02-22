<template>
  <v-card>
    <v-card-text>
      <v-list>
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="title">Solicitudes</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-divider />

        <v-list dense nav>
          <v-list-item v-for="bid in bids" :key="bid.id" two-line nuxt :to="getNewUrl(bid.id)" exact>
            <v-list-item-avatar>
              <v-icon v-if="bid.offer_kind === 'luz'" color="warning">mdi-flash</v-icon>
              <v-icon v-else color="blue">mdi-fire</v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title>
                <small> ID: {{ bid.id }} </small>
                <v-divider vertical />
                <i> {{ bid.status }} </i>
              </v-list-item-title>
              <v-list-item-subtitle>
                {{ bid['fecha_firma'] }}
                <v-list-item-action>
                  <delete-button @click="deleteBid(bid.id)" />
                </v-list-item-action>
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>

          <v-dialog v-model="addNewBidDialog" max-width="750">
            <template v-slot:activator="{ on }">
              <v-list-item v-on="on">
                <v-list-item-avatar>
                  <v-icon color="success">mdi-plus</v-icon>
                </v-list-item-avatar>
                <v-list-item-title>Añadir nuevo solicitud</v-list-item-title>
              </v-list-item>
            </template>

            <add-new-bid
              :user-id="userId"
              @close="addNewBidDialog = false"
              @bid-added="
                $emit('bid-added')
                addNewBidDialog = false
              "
            />
          </v-dialog>
        </v-list>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
import AddNewBid from '@/components/forms/AddNewBid'
import DeleteButton from '@/components/buttons/deleteButton'
export default {
  name: 'SolicitudesBar',
  components: { DeleteButton, AddNewBid },
  props: {
    userId: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      addNewBidDialog: false,
      bids: [],
    }
  },
  async mounted() {
    this.bids = await this.$axios.$get(`/bids/bids/?user=${this.userId}`)
  },
  methods: {
    async deleteBid(bidId) {
      const willDelete = await this.$swal({
        title: `Eliminar solicitud ${bidId}?`,
        text: 'Una vez borrado, no podrás recuperar este solicitud!',
        icon: 'warning',
        buttons: true,
        dangerMode: true,
      })
      if (!willDelete) return
      await this.$axios.$delete(`/bids/bids/${bidId}/`)
      await this.$emit('bid-deleted')
    },
    getNewUrl(bidId) {
      const params = { ...this.$route.query, bid_id: bidId }
      return (
        this.$route.path +
        '?' +
        Object.keys(params)
          .map((key) => {
            return encodeURIComponent(key) + '=' + encodeURIComponent(params[key])
          })
          .join('&')
      )
    },
  },
}
</script>
