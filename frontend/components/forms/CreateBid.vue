<template>
  <v-card>
    <v-card-title> Crear solicitud para cliente {{ forClient }} </v-card-title>
    <v-card-text>
      <v-stepper v-model="stepModel">
        <v-stepper-header>
          <template v-for="(step, idx) in steps">
            <v-stepper-step :key="`${idx}-step`" :complete="stepModel > idx" :step="idx">
              {{ step.text }}
            </v-stepper-step>

            <v-divider v-if="idx !== steps.length" :key="idx"></v-divider>
          </template>
        </v-stepper-header>
        <v-stepper-items>
          <v-stepper-content :step="1">
            <select-offer-form v-model="offer" />
            <v-btn
              v-if="offer"
              block
              color="primary"
              @click="
                stepModel++
                fetchPuntos()
              "
            >
              Continue
            </v-btn>
          </v-stepper-content>
          <v-stepper-content :step="2">
            <v-col v-if="offer">
              <v-row>
                <v-col>
                  <v-btn
                    v-for="p in puntos"
                    :key="p.id"
                    class="pa-2"
                    :color="punto && punto.id === p.id ? 'success' : null"
                    @click="punto = p"
                  >
                    Punto {{ p.id }}. {{ p.name || p.cups_luz || p.cups_gas }}
                  </v-btn>

                  <add-punto-dialog
                    :bid="{ offer }"
                    :offer-client-type="offer.client_type"
                    closeable
                    @punto-added="fetchPuntos"
                  />
                </v-col>
              </v-row>

              <v-row>
                <v-col>
                  <v-btn color="warning" @click="stepModel--">Atras</v-btn>
                  <submit-button label="Guardar" @click="submit" />
                </v-col>
              </v-row>
            </v-col>
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
      steps: [
        {
          text: 'Elejir oferta',
        },
        {
          text: 'Elejir punto',
        },
      ],
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
      } catch (e) {
        console.error(e)
        await this.$swal({ title: 'Error', text: e.response.data, icon: 'error' })
      }
    },
  },
}
</script>
