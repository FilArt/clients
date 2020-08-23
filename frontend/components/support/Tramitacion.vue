<template>
  <div>
    <v-progress-circular v-if="!bid" indermediate />
    <div v-else>
      <detail-offer :offer="bid.offer" />

      <v-divider />

      <v-alert v-if="bid.puntos.length === 0" type="warning">
        No puntos!
      </v-alert>
      <puntos-list v-else :puntos="bid.puntos" />

      <v-divider />

      <v-container v-if="tramitacion">
        <v-row>
          <v-col v-for="group in groups" :key="group.label" cols="12" md="4">
            <v-radio-group v-model="tramitacion[group.value]" :label="group.label" @change="tramitate">
              <v-radio v-for="state in states" :key="state.label" :label="state.label" :value="state.value" />
              <v-btn
                @click="
                  tramitacion[group.value] = null
                  tramitate()
                "
              >
                Resetar?
              </v-btn>
            </v-radio-group>
          </v-col>
        </v-row>
      </v-container>

      <v-divider />

      <v-dialog v-model="historyDialog" max-width="1000">
        <template v-slot:activator="{ on }">
          <v-btn color="pink" block outlined v-on="on" @click="fetchHistory">
            Show history?
            <v-icon right>
              mdi-history
            </v-icon>
          </v-btn>
        </template>
        <v-card>
          <v-card-title>
            <v-row>
              <v-col>
                History
              </v-col>
              <v-col class="flex-grow-0">
                <close-button @click="historyDialog = false" />
              </v-col>
            </v-row>
          </v-card-title>
          <v-card-text v-if="history.length">
            <history-list :history="history" />
          </v-card-text>
        </v-card>
      </v-dialog>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Tramitacion',
  components: {
    CloseButton: () => import('~/components/buttons/closeButton'),
    PuntosList: () => import('~/components/puntos/PuntosList'),
    detailOffer: () => import('~/components/detailOffer'),
    HistoryList: () => import('~/components/history/HistoryList'),
  },
  props: {
    bidId: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      bid: null,
      history: [],
      historyDialog: false,
      tramitacion: null,
      groups: [
        {
          label: 'Documentacion',
          value: 'doc',
        },
        {
          label: 'Llamada',
          value: 'call',
        },
        {
          label: 'Scoring',
          value: 'scoring',
        },
      ],
      states: [
        {
          label: 'Si',
          value: true,
        },
        {
          label: 'No',
          value: false,
        },
      ],
    }
  },
  async mounted() {
    await this.fetchBid()
    await this.fetchTramitacion()
  },
  methods: {
    async fetchHistory() {
      this.history = await this.$axios.$get(`bids/bids/${this.bidId}/history/`)
    },
    async fetchBid() {
      this.bid = await this.$axios.$get(`bids/bids/${this.bidId}/`)
    },
    async fetchTramitacion() {
      if (this.bid.tramitacion) {
        this.tramitacion = await this.$axios.$get(`tramitacion/${this.bid.tramitacion}/`)
      } else {
        this.tramitacion = {
          id: null,
          bid: this.bid.id,
          doc: null,
          call: null,
          scoring: null,
        }
      }
    },
    async tramitate() {
      const message = await this.$swal({
        title: 'Anadir mensaje',
        content: 'input',
      })
      try {
        if (this.tramitacion.id) {
          this.tramitacion = await this.$axios.$patch(`tramitacion/${this.tramitacion.id}/`, {
            ...this.tramitacion,
            message,
          })
        } else {
          this.tramitacion = await this.$axios.$post('tramitacion/', {
            ...this.tramitacion,
            message,
          })
        }
      } catch (e) {
        await this.$swal({
          title: 'Error!',
          text: JSON.stringify(e.response.data),
        })
        return
      }
      await this.fetchBid()
      this.$emit('tramitate', this.bid.status)
    },
  },
}
</script>
