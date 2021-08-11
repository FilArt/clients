<template>
  <v-card>
    <v-card-title> Crear solicitud para cliente {{ forClient }} </v-card-title>
    <v-card-text>
      <v-stepper v-model="stepModel">
        <v-stepper-header>
          <v-stepper-step :complete="!!offer" :step="1"> Elejir oferta </v-stepper-step>
          <v-divider />
          <v-stepper-step :complete="!!punto" :step="2"> Elejir punto </v-stepper-step>
        </v-stepper-header>
        <v-stepper-items>
          <v-stepper-content :step="1">
            <select-offer-form v-model="offer" />
            <v-btn
              :disabled="!offer"
              block
              color="primary"
              @click="
                stepModel++
                fetchPuntos()
              "
            >
              OK
            </v-btn>
          </v-stepper-content>
          <v-stepper-content :step="2">
            <div v-if="offer" tile>
              <v-card-text>
                <v-btn
                  v-for="p in puntos"
                  :key="p.id"
                  class="pa-2"
                  :color="punto && punto.id === p.id ? 'success' : null"
                  @click="punto = p"
                >
                  Punto {{ p.id }}. {{ p.name || p.cups_luz || p.cups_gas }}
                </v-btn>

                <br />
                <br />

                <v-row class="text-center">
                  <v-col>
                    <add-punto-dialog
                      block
                      :user-id="forClient"
                      :bid="{ offer }"
                      :offer-client-type="offer.client_type"
                      closeable
                      @punto-added="fetchPuntos"
                    />
                  </v-col>
                </v-row>
              </v-card-text>

              <hr />

              <v-card-actions>
                <v-btn color="warning" @click="stepModel--">Atras</v-btn>
                <v-spacer />
                <submit-button :disabled="!offer || !punto" label="Guardar" @click="submit" />
              </v-card-actions>
            </div>
          </v-stepper-content>
        </v-stepper-items>
      </v-stepper>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'CreateBid',
  components: {
    SelectOfferForm: () => import('@/components/forms/SelectOfferForm'),
    SubmitButton: () => import('@/components/buttons/submitButton'),
    AddPuntoDialog: () => import('@/components/puntos/AddPuntoDialog'),
  },
  props: {
    forClient: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      offer: null,
      punto: null,
      stepModel: 1,
      puntos: [],
    }
  },
  methods: {
    async fetchPuntos() {
      this.puntos = await this.$axios.$get(`/users/puntos/?user=${this.forClient}`)
    },
    async submit() {
      try {
        await this.$axios.$post('bids/bids/', { user: this.forClient, offer: this.offer.id, punto: this.punto.id })
        this.$emit('bid-added')
        this.$toast.global.done()
        this.offer = this.punto = null
        this.stepModel = 1
      } catch (e) {
        console.error(e)
        await this.$swal({ title: 'Error', text: e.response.data, icon: 'error' })
      }
    },
  },
}
</script>
