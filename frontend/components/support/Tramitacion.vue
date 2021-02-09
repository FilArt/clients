<template>
  <div v-if="bidId && bid">
    <v-dialog v-model="tramitateDialog" max-width="500">
      <v-card>
        <v-row align="center">
          <v-col>
            <v-card-title>Agregar mensajes (opcional) y enviar</v-card-title>
          </v-col>

          <v-col class="flex-grow-0">
            <close-button @click="tramitateDialog = false" />
          </v-col>
        </v-row>

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
      <v-col style="max-width: 750px">
        <v-card-title>
          {{ modeTramitacion ? 'Tramitacion' : 'Facturacion' }}
        </v-card-title>

        <v-row>
          <v-col>
            <v-dialog v-model="offerDetailDialog" max-width="750">
              <template v-slot:activator="{ on }">
                <v-chip style="cursor: pointer" v-on="on">
                  <v-col><v-icon>mdi-eye</v-icon></v-col>
                  <v-col>Oferta</v-col>
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
                </v-chip>
              </template>

              <detail-offer
                :offer="bid.offer"
                closeable
                changeable
                :bid-id="bidId"
                @close="offerDetailDialog = false"
                @offer-changed="fetchBid"
              />
            </v-dialog>
          </v-col>
        </v-row>

        <v-row v-if="['admin', 'support'].includes($auth.user.role)">
          <v-col>
            <v-switch v-if="facturacion && bid" v-model="modeTramitacion" label="Modo tramitacion" />

            <v-row v-if="modeTramitacion">
              <v-col>
                <template
                  v-for="group in groups.filter((g) =>
                    bid.offer_status_accesible ? true : g.value !== 'offer_status',
                  )"
                >
                  <v-radio-group
                    :key="group.label"
                    v-model="bid[group.value]"
                    :style="`border: ${ourColor} solid 1px; border-radius: 10px; padding: 10px;`"
                    @change="tramitateDialog = true"
                  >
                    <v-toolbar>
                      <v-toolbar-title>
                        {{ group.label }}
                      </v-toolbar-title>

                      <v-spacer />

                      <v-toolbar-items class="align-baseline">
                        <template
                          v-for="state in group.value === 'offer_status' ? states.offer_status : states.default"
                        >
                          <v-container :key="state.label">
                            <v-radio
                              :label="state.label"
                              :value="state.value"
                              @click="newStatus = `${state.label} ${group.label}`"
                            />
                          </v-container>
                        </template>
                        <v-btn
                          icon
                          @click="
                            bid[group.value] = null
                            tramitateDialog = true
                          "
                        >
                          <v-icon>mdi-eraser-variant</v-icon>
                        </v-btn>
                      </v-toolbar-items>
                    </v-toolbar>

                    <br />

                    {{ lastComments[group.value] }}
                  </v-radio-group>
                </template>
              </v-col>
            </v-row>

            <facturacion
              v-else
              :bid-id="bid.id"
              :responsible="bid.responsible"
              :canal="bid.canal"
              :default-canal-commission="parseFloat(bid.offer.canal_commission)"
              :default-responsible-commission="parseFloat(bid.offer.agent_commission)"
              :current-responsible-commission="parseFloat(bid.commission)"
              :current-canal-commission="parseFloat(bid.canal_commission)"
              :is-canal-paid="bid.canal_paid"
              :is-responsible-paid="bid.paid"
              @paid="$emit('tramitate')"
            />
          </v-col>
        </v-row>

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
                  <history-list :history="history" @comment-deleted="fetchHistory" />
                </v-card-text>
              </v-card>
            </v-dialog>
          </v-col>
        </v-row>
      </v-col>

      <v-divider vertical />

      <v-col>
        <v-card-title>Punto</v-card-title>
        <punto-item :punto="bid.punto" @punto-updated="fetchBid" @punto-deleted="$emit('punto-deleted')" />
        <add-punto-dialog v-if="!bid.punto" closeable :bid-id="bid.id" @punto-added="fetchBid" />
      </v-col>
    </v-row>
  </div>
</template>

<script>
import constants from '@/lib/constants'

export default {
  name: 'Tramitacion',
  components: {
    PuntoItem: () => import('@/components/puntos/PuntoItem'),
    AddPuntoDialog: () => import('@/components/puntos/AddPuntoDialog'),
    Facturacion: () => import('@/components/support/Facturacion'),
    CloseButton: () => import('@/components/buttons/closeButton'),
    detailOffer: () => import('@/components/detailOffer'),
    HistoryList: () => import('@/components/history/HistoryList'),
  },
  props: {
    facturacion: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      ourColor: constants.ourColor,
      lastComments: {
        doc: '...',
        scoring: '...',
        call: '...',
        offer_status: '...',
      },
      canalVariable: 0,
      agentVariable: 0,
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
        {
          label: 'Estado de oferta',
          value: 'offer_status',
        },
      ],
      // <v-radio label="Firmada" :value="0" @click="newStatus = `Estado de oferta: Firmada`" />
      // <v-radio label="PTE Firmar" :value="1" @click="newStatus = `Estado de oferta: PTE Firmar`" />

      states: {
        default: [
          {
            label: 'OK',
            value: true,
          },
          {
            label: 'KO',
            value: false,
          },
        ],
        offer_status: [
          {
            label: 'Firmada',
            value: 0,
          },
          {
            label: 'PTE Firmar',
            value: 1,
          },
        ],
      },
      bidErrors: {},
      tramitateDialog: false,
      message: '',
      internalMessage: '',
      modeTramitacion: !this.facturacion,
    }
  },
  computed: {
    bidId() {
      const { bid_id } = this.$route.query
      return bid_id
    },
  },
  watch: {
    bidId: {
      handler: async function () {
        await this.refresh()
      },
      deep: true,
    },
  },
  async mounted() {
    await this.refresh()
  },
  methods: {
    async refresh() {
      if (this.bidId && this.bidId.match(/\d+/)) {
        await this.fetchBid()
        if (['admin', 'support'].includes(this.$auth.user.role)) await this.fetchLastComments()
      }
    },
    async fetchHistory() {
      this.history = await this.$axios.$get(`bids/bids/${this.bidId}/history/`)
    },
    async fetchBid() {
      try {
        this.bid = await this.$axios.$get(`bids/bids/${this.bidId}/`)
      } catch (e) {
        if (e.response.status === 403) {
          await this.$swal({ title: 'Permission denied', icon: 'error' })
        }
      }
    },
    async fetchLastComments() {
      this.lastComments = await this.$axios.$get(`bids/bids/${this.bidId}/last_comments/`)
    },
    async tramitate() {
      this.loading = true
      try {
        this.bid = await this.$axios.$patch(`bids/bids/${this.bid.id}/`, {
          doc: this.bid.doc,
          call: this.bid.call,
          scoring: this.bid.scoring,
          offer_status: this.bid.offer_status,
          new_status: this.newStatus,
          message: this.message,
          internal_message: this.internalMessage,
        })
        this.$emit('tramitate')
        await this.fetchLastComments()
        this.$toast.global.done()
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
  },
}
</script>
