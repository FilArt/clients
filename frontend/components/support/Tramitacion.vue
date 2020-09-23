<template>
  <div v-if="bid">
    <snack-bar-it :noty-key="notificationKey" />

    <v-dialog v-model="tramitateDialog" max-width="500">
      <v-card>
        <v-card-title>Agregar mensajes (opcional) y enviar</v-card-title>

        <v-card-text>
          <v-form @submit.prevent="tramitate">
            <v-row>
              <v-col>
                <v-textarea v-model="message" label="Mensaje para cliente" />
              </v-col>
            </v-row>

            <v-row>
              <v-col>
                <v-textarea v-model="internalMessage" label="Mensaje para agente" />
              </v-col>
            </v-row>

            <v-btn block type="submit" :loading="loading" color="success">Enviar</v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-row class="text-center">
      <v-col :style="hidePuntos ? null : 'max-width: 300px'">
        <v-row>
          <v-col>
            <v-dialog v-model="offerDetailDialog" max-width="750">
              <template v-slot:activator="{ on }">
                <v-chip style="cursor: pointer" v-on="on">
                  <v-col>
                    <small>id {{ bid.offer.id }}</small>
                  </v-col>
                  <v-divider vertical />
                  <v-col>
                    <small>{{ bid.offer.company }}</small>
                  </v-col>
                  <v-divider vertical />
                  <v-spacer />
                  <v-col>{{ bid.offer.name }}</v-col>
                  <v-col><v-icon>mdi-information</v-icon></v-col>
                </v-chip>
              </template>

              <v-card>
                <detail-offer :offer="bid.offer" closeable @close="offerDetailDialog = false" />
              </v-card>
            </v-dialog>
          </v-col>
        </v-row>

        <div v-if="['admin', 'tramitacion'].includes($auth.user.role)">
          <v-row v-if="facturacion" align="center">
            <v-col>
              <v-toolbar>Responsable: {{ bid.responsible || '...' }}</v-toolbar>

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

          <v-row v-else>
            <v-col>
              <div v-for="group in groups" :key="group.label">
                <v-radio-group v-model="bid[group.value]" :label="group.label" @change="tramitateDialog = true">
                  <v-row>
                    <v-col v-for="state in states" :key="state.label">
                      <v-radio
                        :label="state.label"
                        :value="state.value"
                        @click="newStatus = `${state.label} ${group.label}`"
                      />
                    </v-col>
                    <v-col>
                      <v-btn
                        icon
                        @click="
                          bid[group.value] = null
                          tramitateDialog = true
                        "
                      >
                        <v-icon>mdi-eraser-variant</v-icon>
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-radio-group>
              </div>
            </v-col>
          </v-row>
        </div>

        <v-row>
          <v-col>
            <v-dialog v-model="historyDialog" max-width="1000">
              <template v-slot:activator="{ on }">
                <v-btn color="pink" outlined v-on="on" @click="fetchHistory">
                  Ver historial
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
          </v-col>
        </v-row>

        <v-row v-if="pushToTitle">
          <v-col>
            <v-btn color="error" @click="$emit('push-to')"> Mover a la {{ pushToTitle }}? </v-btn>
          </v-col>
        </v-row>
      </v-col>

      <v-divider vertical />

      <v-col v-if="!hidePuntos">
        <v-alert v-if="bid.puntos.length === 0" type="warning">No puntos!</v-alert>
        <puntos-list v-else :puntos="bid.puntos" />
      </v-col>
    </v-row>
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
    SnackBarIt: () => import('@/components/snackbar/SnackBarIt'),
  },
  props: {
    pushToTitle: {
      type: String,
      default: null,
    },
    bidId: {
      type: Number,
      default: null,
    },
    facturacion: {
      type: Boolean,
      default: false,
    },
    showPushToKo: {
      type: Boolean,
      default: false,
    },
    hidePuntos: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      offerDetailDialog: false,
      loading: false,
      bid: null,
      newStatus: null,
      history: [],
      historyDialog: false,
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
      notificationKey: 0,
      bidErrors: {},
      tramitateDialog: false,
      message: '',
      internalMessage: '',
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
  async created() {
    await this.fetchBid()
  },
  methods: {
    async fetchHistory() {
      this.history = await this.$axios.$get(`bids/bids/${this.bidId}/history/`)
    },
    async fetchBid() {
      const fields = [
        'id',
        'offer',
        'status',
        'offer',
        'puntos',
        'responsible',
        'paid',
        'doc',
        'scoring',
        'call',
        'commission',
        'agent_type',
      ].join()
      try {
        this.bid = await this.$axios.$get(`bids/bids/${this.bidId}/?fields=${fields}`)
      } catch (e) {
        if (e.response.status === 403) {
          await this.$swal({ title: 'Permission denied', icon: 'error' })
        }
      }
    },
    async tramitate() {
      this.loading = true
      try {
        const bid = await this.$axios.$patch(`bids/bids/${this.bid.id}/`, {
          doc: this.bid.doc,
          call: this.bid.call,
          scoring: this.bid.scoring,
          new_status: this.newStatus,
          message: this.message,
          internal_message: this.internalMessage,
        })
        this.bid = bid
        this.$emit('tramitate')
        this.notificationKey += 1
        this.tramitateDialog = false
        this.message = this.internalMessage = null
      } catch (e) {
        await this.$swal({
          title: 'Error!',
          text: JSON.stringify(e.response.data),
        })
      } finally {
        this.loading = false
      }
    },
    async pagar(field, value) {
      this.bidErrors[field] = null
      try {
        this.bid = await this.$axios.$patch(`bids/bids/${this.bid.id}/`, { [field]: value })
        this.$emit('tramitate')
        this.notificationKey += 1
      } catch (e) {
        const err = e.response.data
        if (err.detail) {
          await this.$swal({ title: 'Error', text: err.detail, icon: 'error' })
        }
        this.bidErrors = err
      }
    },
  },
}
</script>
