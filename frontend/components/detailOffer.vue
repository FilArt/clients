<template>
  <v-card>
    <v-row>
      <v-col>
        <p class="text-center headline">
          {{ hideName ? `Oferta ${offer.id}` : offer.name }}
        </p>
      </v-col>
      <v-col v-if="closeable" class="flex-grow-0">
        <v-btn icon color="error" @click="$emit('close')">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-col>
    </v-row>

    <v-divider />

    <v-row align="center">
      <v-col>
        <v-img class="mx-auto" max-width="150" :src="'/no-image.svg'" />
      </v-col>

      <v-col class="flex-grow-1">
        <v-simple-table style="max-width: 750px" class="pa-3">
          <template v-slot:default>
            <tr>
              <td colspan="2" class="font-weight-light font-italic text-left" style="padding-bottom: 2em">
                {{ offer.description }}
              </td>
            </tr>

            <tr>
              <td>Tarifa:</td>
              <td>{{ offer.tarif }}</td>
            </tr>

            <tr>
              <td>Tipo de oferta:</td>
              <td>
                {{ offer.client_type === 0 ? 'Fisico' : 'Juridico' }}
              </td>
            </tr>

            <tr>
              <td>Tipo de precio:</td>
              <td>{{ offer.is_price_permanent }}</td>
            </tr>

            <br />

            <tr>
              <td :rowspan="powers.length + 1">Precio por potencia:</td>
            </tr>

            <tr v-for="(power, pIdx) in powers" :key="'p' + pIdx">
              <td>{{ power.text }}: {{ power.value }} €</td>
            </tr>

            <br />

            <tr>
              <td :rowspan="consumptions.length + 1">Precio por consumo:</td>
            </tr>
            <tr v-for="(consumption, cIdx) in consumptions" :key="'c' + cIdx">
              <td>{{ consumption.text }}: {{ consumption.value }} €</td>
            </tr>
          </template>
        </v-simple-table>
      </v-col>
    </v-row>

    <v-card-text v-if="changeable">
      Editar oferta
      <v-row align="center">
        <v-col>
          <v-select v-model="kind" :items="['luz', 'gas']" label="Luz o gas?" />
        </v-col>
        <v-col>
          <company-select v-model="company" />
        </v-col>
        <v-col>
          <tarif-select v-model="tarif" :gas="kind === 'gas'" />
        </v-col>
        <v-col>
          <client-type-select v-model="clientType" />
        </v-col>
        <v-col v-if="company && tarif && clientType">
          <offer-select v-model="newOffer" :company="company" :tarif="tarif" :client-type="clientType" />
        </v-col>
      </v-row>

      <v-btn :disabled="!newOffer || newOffer.id === offer.id" block color="success" @click="changeOffer">
        Salvar
      </v-btn>
    </v-card-text>

    <v-card-actions v-else-if="selectable">
      <v-btn rounded block outlined color="primary" @click="replaceBid">
        Elejir
        <v-icon right> mdi-briefcase </v-icon>
      </v-btn>
    </v-card-actions>

    <v-card-actions v-else-if="showAddBtn && $auth.loggedIn && !showCalcDetails">
      <v-btn rounded block outlined color="primary" @click="addBid">
        Añadir a cartera
        <v-icon right> mdi-briefcase </v-icon>
      </v-btn>
    </v-card-actions>

    <calculator-details v-if="showCalcDetails" :offer="offer" />
  </v-card>
</template>

<script>
export default {
  name: 'DetailOffer',
  components: {
    CompanySelect: () => import('@/components/selects/CompanySelect'),
    TarifSelect: () => import('@/components/selects/TarifSelect'),
    ClientTypeSelect: () => import('@/components/selects/ClientTypeSelect'),
    OfferSelect: () => import('@/components/selects/OfferSelect'),
    CalculatorDetails: () => import('@/components/CalculatorDetails'),
  },
  props: {
    bidId: {
      type: [String, Number],
      default: 0,
    },
    changeable: {
      type: [Boolean, String],
      default: false,
    },
    selectable: {
      type: [Boolean, String],
      default: false,
    },
    closeable: {
      type: Boolean,
      default: false,
    },
    showAddBtn: {
      type: Boolean,
      default: false,
    },
    hideName: {
      type: Boolean,
      default: false,
    },
    showCalculatorDetails: {
      type: Boolean,
      default: false,
    },
    offer: {
      type: Object,
      default: () => null,
    },
  },
  data() {
    return {
      company: null,
      tarif: null,
      clientType: null,
      kind: null,
      newOffer: null,
    }
  },
  computed: {
    showCalcDetails() {
      return this.showCalculatorDetails || this.$route.query.showCalculatorDetails
    },
    powers() {
      return ['p1', 'p2', 'p3']
        .filter((power) => this.offer[power])
        .map((power) => {
          return {
            text: power.toUpperCase(),
            value: this.offer[power],
          }
        })
    },
    consumptions() {
      return ['c1', 'c2', 'c3']
        .filter((consumption) => this.offer[consumption])
        .map((consumption) => {
          return {
            text: consumption.replace('c', 'p').toUpperCase(),
            value: this.offer[consumption],
          }
        })
    },
  },
  methods: {
    changeOffer() {
      if (!this.bidId) {
        alert('Error. ' + 'Bid undefined')
        return
      }
      this.$axios.patch(`bids/bids/${this.bidId}/`, { offer: this.newOffer.id }).then(() => {
        this.newOffer = null
        this.$emit('offer-changed')
      })
    },
    replaceBid() {
      const data = { offer: this.offer.id }
      const bidId = this.$store.state.bidToChange
      this.$axios.patch(`bids/bids/${bidId}/`, data).then(() => {
        this.$router.push(`/bids/${bidId}`)
      })
    },
    addBid() {
      if (!this.offer) return
      let data = { offer: this.offer.id }
      if (this.$route.query.fromCalculator === 'true') {
        data = { ...data, ...this.$store.state.calculatorForm }
      }
      this.$axios.$post('bids/bids/', data).then((createdBidData) => {
        this.$swal({
          title: 'Se ha agregado una solicitud de contrato a la cartera.',
          icon: 'success',
          buttons: {
            cancel: true,
            goToPortfel: {
              text: 'Ir a Cartera',
              value: 'bids',
            },
            goToBid: {
              text: 'Contratar',
              value: 'bid',
            },
          },
        }).then((value) => {
          if (value === 'bids') {
            this.$router.push('/bids')
          } else if (value === 'bid') {
            this.$router.push(`/bids/${createdBidData.id}`)
          }
        })
      })
    },
  },
}
</script>
