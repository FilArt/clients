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

        <v-col>
          <v-row v-for="bid in bids" :key="bid.id" align="center" class="pa-0">
            <v-col class="pa-0">
              <v-list-item three-line nuxt :to="getNewUrl(bid.id)" exact class="d-flex align-center">
                <v-list-item-content>
                  <v-list-item-title>
                    <v-icon v-if="bid['offer_kind'] === 'luz'" color="warning">mdi-flash</v-icon>
                    <v-icon v-else color="blue">mdi-fire</v-icon>
                    <small>ID: {{ bid.id }}</small>
                  </v-list-item-title>
                  <v-list-item-title>
                    <i>{{ bid.status }}</i>
                  </v-list-item-title>

                  <v-list-item-subtitle> FF: {{ bid.fecha_firma || '-' }} </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-col>

            <v-col class="flex-grow-0">
              <v-dialog v-if="$auth.user && $auth.user.role === 'admin'" v-model="dialogs[bid.id]" max-width="500px">
                <template v-slot:activator="{ on }">
                  <v-btn color="info" icon v-on="on"><v-icon>mdi-pencil</v-icon></v-btn>
                </template>
                <v-card>
                  <v-card-title> Fecha firma </v-card-title>
                  <v-card-text>
                    <v-row>
                      <v-col>
                        <date-time-filter v-model="bid['fecha_firma']" format="DD/MM/YYYY HH:mm" inline />
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col class="flex-grow-0">
                        <v-btn color="warning" @click="dialogs[bid.id] = false"> Cancellar </v-btn>
                      </v-col>
                      <v-col>
                        <v-btn block color="info" @click="updateBid(bid.id, 'fecha_firma', bid['fecha_firma'])">
                          Salvar
                        </v-btn>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
              </v-dialog>

              <delete-button v-if="allowDelete" @click="deleteBid(bid.id)" />
            </v-col>
          </v-row>

          <v-row>
            <v-col>
              <add-new-bid-dialog
                :user-id="userId"
                label="Añadir nuevo solicitud"
                @bid-added="
                  $emit('bid-added')
                  fetchBids()
                "
              />
            </v-col>
          </v-row>
        </v-col>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
import AddNewBidDialog from '@/components/dialogs/AddNewBidDialog'
import DeleteButton from '@/components/buttons/deleteButton'
import { mapState } from 'vuex'
import DateTimeFilter from '@/components/DateTimeFilter'
import { parse } from 'date-fns'
export default {
  name: 'SolicitudesBar',
  components: { DateTimeFilter, DeleteButton, AddNewBidDialog },
  props: {
    userId: {
      type: Number,
      default: null,
    },
    allowDelete: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      addNewBidDialog: false,
      dialogs: {},
    }
  },
  computed: mapState({ bids: (state) => state.bids.bids }),
  async mounted() {
    await this.fetchBids()
  },
  methods: {
    async fetchBids() {
      await this.$store.dispatch('bids/fetchBids', { params: `user=${this.userId}` })
    },
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
    async updateBid(bidId, field, value) {
      value = parse(value, 'dd/MM/yyyy HH:mm', new Date())
      await this.$axios.$patch(`/bids/bids/${bidId}/`, { [field]: value })
      await this.fetchBids()
      this.dialogs[bidId] = false
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
