<template>
  <div>
    <v-snackbar v-model="snackbar" right bottom :timeout="2500" color="success">
      {{ snackbarTitle }}

      <template v-slot:action="{ attrs }">
        <v-btn text v-bind="attrs" @click="snackbar = false"> Cerrar </v-btn>
      </template>
    </v-snackbar>

    <div>
      <v-divider />

      <v-card-text>
        <v-list>
          <v-list-group>
            <template v-slot:activator>
              <v-list-item-content>
                <v-chip style="cursor: pointer">
                  <v-col>
                    <small>id {{ bid.offer.id }}</small>
                  </v-col>
                  <v-divider vertical />
                  <v-col>
                    <small>{{ bid.offer.company }}</small>
                  </v-col>
                  <v-divider vertical />
                  <v-spacer />
                  <v-col>
                    {{ bid.offer.name }}
                  </v-col>
                </v-chip>
              </v-list-item-content>
            </template>

            <v-list-item>
              <detail-offer :offer="bid.offer" />
            </v-list-item>
          </v-list-group>
        </v-list>
      </v-card-text>

      <v-divider />

      <v-alert v-if="bid.puntos.length === 0" type="warning">No puntos!</v-alert>
      <puntos-list v-else :puntos="bid.puntos" />

      <v-divider />

      <v-container v-if="['admin', 'tramitacion'].includes($auth.user.role) && tramitacion">
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

        <v-row align="center">
          <v-col>
            <v-toolbar> Responsable: {{ bid.responsible || '...' }} </v-toolbar>

            {{ bid.agent_type }}

            <v-radio-group
              :value="commissions.map((c) => c.value).indexOf(bid.commission)"
              label="Comisiones"
              @change="pagar('commission', commissions[$event].value)"
            >
              <v-radio v-for="(commission, idx) in commissions" :key="idx" :value="idx" :label="commission.text" />
              <v-text-field
                v-model="bid.commission"
                label="Variable"
                append-icon="mdi-content-save"
                prepend-icon="mdi-currency-eur"
                @click:append="pagar('commission', bid.commission)"
              />
            </v-radio-group>
          </v-col>

          <v-spacer />

          <v-col>
            <v-radio-group v-model="bid.paid" :error-messages="bidErrors.paid" @change="pagar('paid', bid.paid)">
              <v-radio label="Pagado" :value="true" color="success" />
              <v-radio label="Pendiente" :value="false" color="error" />
            </v-radio-group>
          </v-col>
        </v-row>
      </v-container>

      <v-divider />

      <v-dialog v-model="historyDialog" max-width="1000">
        <template v-slot:activator="{ on }">
          <v-btn color="pink" block outlined v-on="on" @click="fetchHistory">
            Show history?
            <v-icon right>mdi-history</v-icon>
          </v-btn>
        </template>
        <v-card>
          <v-card-title>
            <v-row>
              <v-col>History</v-col>
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
          label: 'OK',
          value: true,
        },
        {
          label: 'KO',
          value: false,
        },
      ],
      snackbar: false,
      snackbarTitle: null,
      bidErrors: {},
    }
  },
  computed: {
    commissions() {
      const { agent_commission, canal_commission } = this.bid.offer
      const result = []
      const agentType = this.bid.agent_type
      if (agentType === 'agent' || agentType === null) {
        result.push({
          text: `Agente comisiones: ${agent_commission} €`,
          value: agent_commission,
        })
      } else if (agentType === 'canal') {
        result.push({
          text: `Canal comisiones: ${canal_commission} €`,
          value: canal_commission,
        })
      }
      return result
    },
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
      const fields = [
        'id',
        'offer',
        'tramitacion',
        'status',
        'offer',
        'puntos',
        'responsible',
        'paid',
        'commission',
        'agent_type',
      ].join()
      this.bid = await this.$axios.$get(`bids/bids/${this.bidId}/?fields=${fields}`)
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
      this.snackbarit()
    },
    async pagar(field, value) {
      this.bidErrors[field] = null
      try {
        const bid = await this.$axios.$patch(`bids/bids/${this.bid.id}/`, { [field]: value })
        this.bid = bid
        this.$emit('tramitate', bid.status)
        this.snackbarit()
      } catch (e) {
        const err = e.response.data
        if (err.detail) {
          await this.$swal({ title: 'Error', text: err.detail, icon: 'error' })
        }
        this.bidErrors = err
      }
    },
    snackbarit(title) {
      if (this.snackbar) this.snackbar = false
      this.snackbarTitle = title || 'Listo!'
      this.snackbar = true
    },
  },
}
</script>
