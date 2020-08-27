<template>
  <div v-if="calculations.tax">
    <v-card min-width="45%" class="mx-auto" max-width="500px">
      <v-card-title style="padding-bottom: 0"> Termino de potencia </v-card-title>

      <v-card-text style="line-height: 2px">
        <v-row v-for="number in [1, 2, 3]" :key="number" align="center">
          <div v-if="calculations[`c_st_p${number}`]" class="d-flex">
            <div class="popusk"></div>
            <v-col class="font-weight-bold flex-grow-0">P{{ number }}</v-col>
            <div class="popusk"></div>
            <v-col style="font-size: 12px">{{ calculations[`c_st_p${number}`] }}</v-col>
          </div>
        </v-row>
      </v-card-text>

      <v-card-title style="padding-bottom: 0"> Termino de energia </v-card-title>

      <v-card-text style="line-height: 2px">
        <v-row v-for="number in [1, 2, 3]" :key="number" align="center">
          <div v-if="calculations[`c_st_p${number}`]" class="d-flex">
            <div class="popusk"></div>
            <v-col class="font-weight-bold flex-grow-0 text-no-wrap">P{{ number }}</v-col>
            <div class="popusk"></div>
            <v-col class="text-no-wrap" style="font-size: 12px">{{ calculations[`c_st_c${number}`] }}</v-col>
          </div>
        </v-row>
      </v-card-text>

      <v-card-title style="padding-bottom: 0"> Otros conceptos </v-card-title>

      <v-card-text style="line-height: 2px">
        <v-row align="center">
          <div class="popusk"></div>
          <v-col class="popusk-2 font-weight-bold text-no-wrap">
            Impuesto eléctrico ({{ calculations.tax.percent }}%)
          </v-col>
          <v-col style="font-size: 12px"> {{ calculations.tax.value }}</v-col>
        </v-row>

        <v-row align="center">
          <div class="popusk"></div>
          <v-col class="popusk-2 flex-shrink-0 font-weight-bold text-no-wrap"> Alquiler de equipos </v-col>
          <v-col class="text-no-wrap" style="font-size: 12px">
            {{ calculations.rental }}
          </v-col>
        </v-row>

        <v-row align="center">
          <div class="popusk"></div>
          <v-col class="popusk-2 font-weight-bold text-no-wrap"> IVA general ({{ calculations.iva.percent }}%) </v-col>
          <v-col class="text-no-wrap" style="font-size: 12px">
            {{ calculations.iva.value }}
          </v-col>
        </v-row>
      </v-card-text>

      <v-card-text class="text-h6 text-right" style="">
        <hr />
        Total factura: {{ calculations.total }}
      </v-card-text>

      <v-card-text class="text-center overline red--text font-weight-bold" style="font-size: 18px !important">
        Paga actualmente: {{ calculations.current_price }} €
      </v-card-text>

      <v-card-text>
        <v-alert border="left" color="#004680" dark>
          <div class="text-uppercase text-center font-weight-thin" style="font-size: 22px !important">
            <p>Ahorro en cada factura</p>
            <p>
              <span class="font-weight-bold">{{ calculations.profit }} ({{ calculations.profit_percent }}%)</span>
            </p>
            <p>Ahorro en anual</p>
            <p>
              <span class="font-weight-bold">{{ calculations.annual_total }}</span>
            </p>
          </div>
        </v-alert>
      </v-card-text>
    </v-card>

    <v-card-actions v-if="$auth.loggedIn">
      <v-btn rounded block outlined color="primary" @click="addBid">
        Añadir a cartera
        <v-icon right> mdi-briefcase </v-icon>
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script>
import { mapState } from 'vuex'
export default {
  name: 'CalculatorDetails',
  props: {
    offer: {
      type: Object,
      default: () => null,
    },
  },
  data() {
    return {
      calculations: [],
    }
  },
  computed: {
    ...mapState({
      form: (state) => state.calculatorForm,
      tarif: (state) => state.tarif,
    }),
  },
  async mounted() {
    await this.getDetails()
  },
  methods: {
    async getDetails() {
      if (!this.offer || !this.form || !this.tarif) return
      this.calculations = await this.$axios.$post('calculator/calculate', {
        ...this.form,
        id: this.offer.id,
        tarif: this.tarif,
        with_calculations: true,
      })
      this.$emit('calculations', this.calculations)
    },
    addBid() {
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

<style scoped>
.popusk {
  width: 2em;
}
.popusk-2 {
  flex-grow: 1;
}
@media only screen and (max-width: 768px) {
  /* For mobile phones: */
  .popusk {
    width: 0;
  }
  .popusk-2 {
    flex-grow: 3;
  }
}
</style>
