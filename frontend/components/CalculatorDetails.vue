<template>
  <v-card>
    <v-card-title>Comparativa de facturas</v-card-title>
    <v-card-text v-if="calculations.tax">
      <v-row align="center">
        <v-col cols="12" lg="6">
          <v-card shaped elevation="12">
            <v-card-title>
              <h4></h4>
            </v-card-title>
            <v-list dense>
              <v-list-item>
                <v-list-item-content>Comercializadora</v-list-item-content>
                <v-list-item-content class="align-end">{{
                  calculations.company_name
                }}</v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>Oferta</v-list-item-content>
                <v-list-item-content class="align-end">{{
                  calculations.name
                }}</v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>Tarifa</v-list-item-content>
                <v-list-item-content class="align-end">{{
                  calculations.tarif
                }}</v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card>
        </v-col>

        <v-col cols="12" lg="6">
          <v-card shaped elevation="12">
            <v-card-title>
              <h4>Termino de potencia</h4>
            </v-card-title>
            <v-list dense>
              <v-list-item>
                <v-list-item-content>P1</v-list-item-content>
                <v-list-item-content class="align-end">{{
                  calculations.c_st_p1
                }}</v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>P2</v-list-item-content>
                <v-list-item-content class="align-end">{{
                  calculations.c_st_p2
                }}</v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>P3</v-list-item-content>
                <v-list-item-content class="align-end">{{
                  calculations.c_st_p3
                }}</v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card>
        </v-col>

        <v-col cols="12" lg="6">
          <v-card shaped elevation="12">
            <v-card-title>
              <h4>Termino de energia</h4>
            </v-card-title>
            <v-list dense>
              <v-list-item>
                <v-list-item-content>P1</v-list-item-content>
                <v-list-item-content class="align-end">{{
                  calculations.c_st_c1
                }}</v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>P2</v-list-item-content>
                <v-list-item-content class="align-end">{{
                  calculations.c_st_c2
                }}</v-list-item-content>
              </v-list-item>
              <v-list-item>
                <v-list-item-content>P3</v-list-item-content>
                <v-list-item-content class="align-end">{{
                  calculations.c_st_c3
                }}</v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card>
        </v-col>

        <v-col cols="12" lg="6">
          <v-card shaped elevation="12">
            <v-card-title>
              <h4>Otros conceptos</h4>
            </v-card-title>
            <v-list dense>
              <v-list-item>
                <v-list-item-content
                  >Impuesto eléctrico ({{
                    calculations.tax.percent
                  }}%)</v-list-item-content
                >
                <v-list-item-content class="align-end"
                  >{{ calculations.tax.value }} €</v-list-item-content
                >
              </v-list-item>

              <v-list-item>
                <v-list-item-content>Alquiler de equipos</v-list-item-content>
                <v-list-item-content class="align-end"
                  >{{ calculations.after_rental }} €</v-list-item-content
                >
              </v-list-item>

              <v-list-item>
                <v-list-item-content
                  >IVA general ({{
                    calculations.iva.percent
                  }}%)</v-list-item-content
                >
                <v-list-item-content class="align-end"
                  >{{ calculations.iva.value }} €</v-list-item-content
                >
              </v-list-item>
            </v-list>
          </v-card>
        </v-col>
      </v-row>

      <v-row cols="12" lg="6">
        <v-col>
          <v-card elevation="12">
            <v-card-title style="color: green;">
              Total factura: {{ calculations.total }} €
            </v-card-title>

            <v-card-title style="color: red;">
              Paga actualmenta: {{ calculations.current_price }} €
            </v-card-title>
          </v-card>
        </v-col>
      </v-row>

      <v-row cols="12" lg="6">
        <v-col>
          <v-card elevation="12">
            <v-card-text>
              <ul>
                <li>
                  <v-card-title>
                    Ahorro en factura: {{ calculations.profit }} € ~=
                    {{ calculations.profit_percent }}%
                  </v-card-title>
                </li>
                <li>
                  <v-card-title>
                    Ahorro en anual: {{ calculations.annual_total }} €
                  </v-card-title>
                </li>
              </ul>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-card-text>

    <v-card-actions>
      <v-btn rounded block outlined color="primary" @click="addBid">
        Añadir a cartera
        <v-icon right>mdi-briefcase</v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>
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
  computed: mapState({
    form: (state) => state.calculatorForm,
    tarif: (state) => state.tarif,
  }),
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
