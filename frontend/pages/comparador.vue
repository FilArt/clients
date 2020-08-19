<template>
  <v-card flat>
    <calculator
      v-if="show === 'calc'"
      hide-offer-names
      @offer-choosed="
        offer = $event
        show = 'detail'
      "
    />

    <div v-else-if="show === 'detail'">
      <detail-offer :offer="offer" hide-name />
      <calculator-details :offer="offer" />

      <div class="d-flex align-center justify-center flex-wrap text-center">
        <v-hover>
          <template v-slot="{ hover }">
            <v-card
              style="border: 5px solid green; color: green;"
              :elevation="hover ? 24 : 2"
              class="pa-3 ma-3"
              @click="show = 'assis'"
            >
              <v-card-title class="text-h5 text-no-wrap">Contractar online</v-card-title>
            </v-card>
          </template>
        </v-hover>

        <v-hover>
          <template v-slot="{ hover }">
            <v-card
              dark
              style="border: 5px solid red;"
              color="success darken-2"
              :elevation="hover ? 24 : 2"
              class="pa-3 ma-3"
              @click="show = 'online'"
            >
              <v-card-title class="text-h5 text-no-wrap">Obtener una consulta</v-card-title>
            </v-card>
          </template>
        </v-hover>
      </div>
    </div>

    <v-row v-if="['calc', 'online', 'assis'].includes(show)" style="margin-top: 2cm;">
      <v-col>
        <v-row>
          <v-col>
            <contract-online
              :show-additional-fields="show === 'assis'"
              :with-factura="show === 'calc'"
              :offer="offer"
            />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
    <v-row>
      <v-spacer />
      <v-col class="text-center">
        <return-button v-if="show !== 'calc'" :to="null" @click="back" />
      </v-col>
      <v-spacer />
    </v-row>
  </v-card>
</template>
<script>
export default {
  auth: 'guest',
  components: {
    Calculator: () => import('../components/forms/Calculator'),
    ReturnButton: () => import('../components/buttons/returnButton'),
    detailOffer: () => import('../components/detailOffer'),
    ContractOnline: () => import('../components/forms/ContractOnline'),
    CalculatorDetails: () => import('../components/CalculatorDetails'),
  },
  data() {
    return {
      offer: null,
      show: 'calc',
    }
  },
  methods: {
    back() {
      switch (this.show) {
        case 'detail':
          this.show = 'calc'
          break
        case 'online':
          this.show = 'detail'
          break
        case 'assis':
          this.show = 'detail'
          break
        default:
          this.show = 'calc'
          break
      }
    },
  },
}
</script>
