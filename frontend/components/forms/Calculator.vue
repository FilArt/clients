<template>
  <v-card :loading="loading" flat class="d-flex flex-column align-center">
    <v-alert v-show="showResults && !offers.length" type="warning">Nohay ofertas</v-alert>
    <v-data-table
      v-show="showResults && offers.length"
      :headers="headers"
      :items="offers"
      @click:row="$auth.loggedIn ? $router.push(getDetailUrl($event)) : $emit('offer-choosed', $event)"
    >
      <template v-slot:[`item.company_logo`]="{ item }">
        <v-avatar width="100">
          <v-img :src="item.company_logo || '/no-image.svg'" />
        </v-avatar>
      </template>

      <template v-slot:[`item.profit_num`]="{ item }"> {{ item.profit_num }} € </template>
      <template v-slot:[`item.annual_total_num`]="{ item }"> {{ item.annual_total_num }} € </template>

      <template v-if="$auth.loggedIn" v-slot:[`item.actions`]="{ item }">
        <v-btn icon nuxt :to="getDetailUrl(item)">
          <v-icon>mdi-eye</v-icon>
        </v-btn>
      </template>
    </v-data-table>
    <v-card v-show="!showResults">
      <v-card-text>
        <v-form novalidate @submit.prevent="submit">
          <v-card class="text-center flex-row flex-nowrap d-flex">
            <v-btn
              :color="form.kind === 'luz' ? ourColor : null"
              :style="`width: 50%; ${form.kind === 'gas' ? 'opacity: 50%' : null}`"
              @click="
                updateForm('kind', 'luz')
                tarif = null
              "
            >
              <v-card-title>Luz</v-card-title>
              <v-icon large color="blue" right>mdi-flash</v-icon>
            </v-btn>

            <v-btn
              :style="`width: 50%; ${form.kind === 'luz' ? 'opacity: 50%' : null}`"
              :color="form.kind === 'gas' ? ourColor : null"
              @click="
                updateForm('kind', 'gas')
                tarif = null
              "
            >
              <v-card-title>Gas</v-card-title><v-icon large color="red" right>mdi-fire</v-icon>
            </v-btn>
          </v-card>

          <v-row align="center" class="text-center">
            <v-col>
              Impuestas
              <v-btn-toggle :value="form.igic" :color="ourColor" @change="updateForm('igic', $event)">
                <v-btn :value="false">Peninsula</v-btn>
                <v-btn :value="true">Islas Canarias</v-btn>
              </v-btn-toggle>
            </v-col>
            <v-col>
              Tipo de cliente
              <br />
              <client-type-select
                :value="form.client_type"
                :error-messages="errorMessages.client_type"
                hint
                @input="updateForm('client_type', $event)"
              />
            </v-col>
          </v-row>

          <v-row align="center">
            <v-col>
              <company-select
                :value="form.company"
                :error-messages="errorMessages.company"
                label="Comercializadora actual"
                hint
                @input="updateForm('company', $event)"
              />
            </v-col>

            <v-col>
              <tarif-select v-model="tarif" :error-messages="errorMessages.tarif" hint :gas="form.kind === 'gas'" />
            </v-col>
          </v-row>

          <v-row>
            <v-col>
              <v-text-field
                label="Periodo"
                name="period"
                suffix="dias"
                dense
                :value="form.period"
                :error-messages="errorMessages.period"
                @input="updateForm('period', $event)"
              >
                <template v-slot:append-outer>
                  <v-tooltip bottom open-on-hover open-on-focus open-on-click>
                    <template v-slot:activator="{ on }">
                      <v-btn icon color="#004680" v-on="on">
                        <v-icon>mdi-information</v-icon>
                      </v-btn>
                    </template>
                    <span>
                      En este campo, ingrese el período (en días) por el cual se le factura. Está información puede
                      obtenerse en su factura.
                    </span>
                  </v-tooltip>
                </template>
              </v-text-field>
            </v-col>

            <v-col>
              <v-text-field
                label="Cadidad de pago en la factura actual"
                name="current_price"
                prefix="€"
                dense
                :value="form.current_price"
                :error-messages="errorMessages.current_price"
                @input="updateForm('current_price', $event)"
              />
            </v-col>
          </v-row>

          <v-row v-if="form.kind === 'luz'">
            <v-col v-for="letter in ['p', 'c']" :key="letter">
              <v-row v-for="number in [1, 2, 3]" :key="number">
                <v-col v-show="showInput(letter, number)">
                  <v-text-field
                    dense
                    :suffix="letter === 'p' ? 'kw' : 'kW/h'"
                    :value="form[letter + number]"
                    :label="(letter === 'p' ? 'Potencia' : 'Consumo') + ' P' + number"
                    :name="'P' + number"
                    :error-messages="errorMessages[letter + number]"
                    @input="updateForm(letter + number, $event)"
                  >
                    <template v-slot:append-outer>
                      <v-tooltip bottom open-on-click open-on-focus open-on-hover z-index="1000">
                        <template v-slot:activator="{ on }">
                          <v-btn icon color="#004680" v-on="on">
                            <v-icon>mdi-information</v-icon>
                          </v-btn>
                        </template>
                        <span>
                          {{
                            letter === 'p'
                              ? 'Ingrese aquí la potencia contratada en kw. Está información puede obtenerse en su factura'
                              : 'Ingrese aquí la energía consumida en kw para cada período. Está información puede obtenerse en su factura.'
                          }}
                        </span>
                      </v-tooltip>
                    </template>
                  </v-text-field>
                </v-col>
              </v-row>
            </v-col>
          </v-row>

          <v-row v-else>
            <v-col>
              <v-text-field
                label="Consumo"
                suffix="kW/h"
                dense
                :value="form.c1"
                :error-messages="errorMessages.c1"
                @input="updateForm('c1', $event)"
              />
            </v-col>
          </v-row>

          <v-row v-if="form.kind === 'luz'">
            <v-col>
              <v-text-field
                suffix="kW"
                label="Energía reactiva (opcional)"
                dense
                :value="form.reactive"
                :error-messages="errorMessages.reactive"
                @input="updateForm('reactive', $event)"
              />
            </v-col>
          </v-row>

          <v-row>
            <submit-button block label="Comparar" />
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>

    <v-card-actions v-show="showResults">
      <v-spacer />
      <return-button :to="null" @click="showResults = false" />
    </v-card-actions>
  </v-card>
</template>
<script>
import constants from '@/lib/constants'

export default {
  name: 'Calculator',
  components: {
    ClientTypeSelect: () => import('~/components/selects/ClientTypeSelect'),
    TarifSelect: () => import('~/components/selects/TarifSelect'),
    CompanySelect: () => import('~/components/selects/CompanySelect'),
    SubmitButton: () => import('~/components/buttons/submitButton'),
    ReturnButton: () => import('~/components/buttons/returnButton'),
  },
  props: {
    hideOfferNames: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      ourColor: constants.ourColor,
      errorMessages: {},
      loading: false,
      showResults: false,
    }
  },
  computed: {
    offers() {
      return this.$store.state.calculatedOffers
    },
    form() {
      return this.$store.state.calculatorForm
    },
    tarif: {
      set(val) {
        this.$store.commit('setTarif', val)
      },
      get() {
        return this.$store.state.tarif
      },
    },
    headers() {
      const _headers = [
        {
          value: 'company_logo',
          sortable: false,
          align: 'left',
        },
        {
          text: 'Oferta',
          value: 'name',
        },
        {
          text: 'Comercializadora',
          value: 'company_name',
        },
        {
          text: 'Ahorro en factura',
          value: 'profit_num',
        },
        {
          text: 'Ahorro anual',
          value: 'annual_total_num',
        },
        {
          value: 'actions',
          sortable: false,
        },
      ]
      return this.hideOfferNames
        ? _headers.map((h) => ({ ...h, value: h.value === 'name' ? 'id' : h.value }))
        : _headers
    },
  },
  methods: {
    getDetailUrl(offer) {
      return `/ofertas/${offer.client_type === 0 ? 'hogar' : 'pyme'}/${offer.id}/?id=${
        offer.id
      }&showCalculatorDetails=true`
    },
    showInput(letter, number) {
      return (
        number === 1 ||
        ['3.0A', '3.1A'].includes(this.tarif) ||
        (letter + number === 'c3' && ['2.1DHA', '2.0DHA'].includes(this.tarif))
      )
    },
    updateForm(key, value) {
      this.$store.commit('updateCalculatorForm', {
        key,
        value,
      })
    },
    submit() {
      this.errorMessages = {}
      this.loading = true
      this.$axios
        .$post('calculator/calculate', {
          tarif: this.tarif,
          ...Object.fromEntries(Object.entries(this.form).filter((i) => [undefined, null, ''].indexOf(i[1]) === -1)),
        })
        .then((data) => {
          this.$store.commit('setCalculatedOffers', data)
          this.showResults = true
        })
        .catch((e) => {
          if (e.response.status !== 400) this.$swal({ title: 'Error', text: String(e), icon: 'error' })
          this.errorMessages = e.response.data
        })
        .finally(() => (this.loading = false))
    },
  },
}
</script>

<style scoped>
.switcher {
  display: flex;
  flex-direction: row;
  justify-content: center;
}

.luz-gas {
  margin: 0 3em 0 3em;
}

@media only screen and (max-width: 768px) {
  .switcher :nth-child(1) {
    padding-bottom: 0;
    padding-top: 0;
  }
  .switcher :nth-child(2) {
    padding-bottom: 0;
    padding-top: 0;
    order: 2;
  }
  .switcher :nth-child(3) {
    padding-bottom: 0;
    padding-top: 0;
    order: 1;
  }
  .luz-gas {
    margin: 0;
  }
}
</style>
