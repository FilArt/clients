<template>
  <v-container>
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
              <v-card-title class="text-h5 text-no-wrap">
                Contractar online
              </v-card-title>
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
              <v-card-title class="text-h5 text-no-wrap">
                Obtener una consulta
              </v-card-title>
            </v-card>
          </template>
        </v-hover>
      </div>
    </div>

    <contract-online v-else-if="show === 'online'" :offer="offer" />

    <contract-online v-else-if="show === 'assis'" show-additional-fields :offer="offer" />

    <v-row>
      <v-col>
        <return-button v-if="show !== 'calc'" :to="null" @click="back" />
      </v-col>
    </v-row>
  </v-container>
</template>
<script>
import Calculator from '~/components/forms/Calculator'
import ReturnButton from '~/components/buttons/returnButton'

export default {
  auth: 'guest',
  components: {
    Calculator,
    ReturnButton,
    detailOffer: () => import('~/components/detailOffer'),
    ContractOnline: () => import('~/components/forms/ContractOnline'),
    CalculatorDetails: () => import('~/components/CalculatorDetails'),
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
