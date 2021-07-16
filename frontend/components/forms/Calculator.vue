<template>
  <v-card :loading="loading" flat class="d-flex flex-column align-center">
    <v-alert v-if="showResults && !offers.length" type="warning">Nohay ofertas</v-alert>

    <calculator-details
      v-else-if="offer"
      :offer="offer"
      @return="
        offer = null
        showResults = true
      "
    />

    <v-data-table v-else-if="showResults && offers.length" :headers="headers" :items="offers" :sort-by="['total']">
      <template v-slot:[`item.company_logo`]="{ item }">
        <v-avatar width="100">
          <v-img :src="item['company_logo'] || '/no-image.svg'" />
        </v-avatar>
      </template>

      <template v-slot:[`item.profit_num`]="{ item }"> {{ item['profit_num'] }} € </template>
      <template v-slot:[`item.annual_profit_num`]="{ item }"> {{ item['annual_profit_num'] }} € </template>

      <template v-slot:[`item.actions`]="{ item }">
        <v-btn
          icon
          @click="
            showResults = false
            offer = item
          "
        >
          <v-icon>mdi-eye</v-icon>
        </v-btn>
      </template>
    </v-data-table>

    <v-card v-else>
      <v-card-text>
        <v-form novalidate @submit.prevent="submit">
          <v-card class="text-center flex-row flex-nowrap d-flex">
            <v-btn
              :color="form.kind === 'luz' ? ourColor : null"
              :style="`width: 50%; ${form.kind === 'gas' ? 'opacity: 50%' : null}`"
              @click="
                form.kind = 'luz'
                form.tarif = null
              "
            >
              <v-card-title>Luz</v-card-title>
              <v-icon large color="blue" right>mdi-flash</v-icon>
            </v-btn>

            <v-btn
              :style="`width: 50%; ${form.kind === 'luz' ? 'opacity: 50%' : null}`"
              :color="form.kind === 'gas' ? ourColor : null"
              @click="
                form.kind = 'gas'
                form.tarif = null
              "
            >
              <v-card-title>Gas</v-card-title><v-icon large color="red" right>mdi-fire</v-icon>
            </v-btn>
          </v-card>

          <v-row align="center" class="text-center">
            <v-col>
              Impuestos
              <v-btn-toggle v-model="form.igic" mandatory :value="form.igic || false" :color="ourColor">
                <v-btn :value="false">Península</v-btn>
                <v-btn :value="true">Islas Canarias</v-btn>
              </v-btn-toggle>
              <v-alert v-if="errorMessages.igic" type="error">
                {{ errorMessages.igic.join('; ') }}
              </v-alert>
            </v-col>
            <v-col>
              Tipo de cliente
              <br />
              <client-type-select
                v-model="form.client_type"
                :error-messages="errorMessages.client_type"
                hint
                without-autonomo
              />
            </v-col>
          </v-row>

          <v-row align="center">
            <v-col>
              <company-select
                v-model="form.company"
                :error-messages="errorMessages.company"
                label="Comercializadora actual"
                hint
              />
            </v-col>

            <v-col>
              <tarif-select
                v-model="form.tarif"
                :error-messages="errorMessages.tarif"
                hint
                :gas="form.kind === 'gas'"
              />
            </v-col>
          </v-row>

          <v-row>
            <v-col>
              <v-text-field
                v-model.number="form.period"
                label="Periodo"
                name="period"
                suffix="dias"
                dense
                :error-messages="errorMessages.period"
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
              <decimal-field
                v-model="form.current_price"
                label="Cadidad de pago en la factura actual"
                name="current_price"
                prefix="€"
                dense
                :error-messages="errorMessages.current_price"
              />
            </v-col>
          </v-row>

          <v-row v-if="form.kind === 'luz'">
            <v-col v-for="letter in ['p', 'c']" :key="letter">
              <v-row v-for="number in [1, 2, 3, 4, 5, 6]" :key="number">
                <v-col v-show="showInput(letter, number)">
                  <decimal-field
                    v-model="form['u' + letter + number]"
                    dense
                    :suffix="letter === 'p' ? 'kw' : 'kW/h'"
                    :label="(letter === 'p' ? 'Potencia' : 'Consumo') + ' P' + number"
                    :name="'P' + number"
                    :error-messages="errorMessages['u' + letter + number]"
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
                  </decimal-field>
                </v-col>
              </v-row>
            </v-col>
          </v-row>

          <v-row v-else>
            <v-col>
              <decimal-field
                v-model="form.uc1"
                label="Consumo"
                suffix="kW/h"
                dense
                :error-messages="errorMessages.c1"
              />
            </v-col>
          </v-row>

          <v-row>
            <v-col>
              <decimal-field
                v-model="form.pago_power"
                label="Pago de potencia"
                prefix="€"
                :error-messages="errorMessages.pago_power"
              />
            </v-col>
            <v-col>
              <decimal-field
                v-model="form.pago_consumption"
                label="Pago de consumo"
                prefix="€"
                :error-messages="errorMessages.pago_consumption"
              />
            </v-col>
          </v-row>

          <v-row>
            <v-col>
              <decimal-field
                v-model="form.annual_consumption"
                label="Consumo annual"
                prefix="kW"
                :error-messages="errorMessages.annual_consumption"
              />
            </v-col>
          </v-row>

          <v-row v-if="form.kind === 'luz' && form.tarif !== '2.0TD'" align="center">
            <v-col>
              <v-checkbox
                v-model="hasReactiveEnergy"
                label="Energía reactiva (opcional)"
                @click="form.reactive = hasReactiveEnergy ? form.reactive : 0"
              />
            </v-col>

            <v-col v-show="hasReactiveEnergy">
              <decimal-field
                v-model="form.reactive"
                prefix="€"
                label="Cadidad de pago energía reactiva"
                :error-messages="errorMessages.reactive"
              />
            </v-col>
          </v-row>

          <v-card-actions>
            <v-btn icon color="warning" @click="resetForm">
              <v-icon>mdi-eraser-variant</v-icon>
            </v-btn>
            <submit-button block label="Comparar" />
          </v-card-actions>
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
const defaultForm = Object.freeze({
  client_type: 1,
  kind: 'luz',
  tarif: null,
  period: 0,
  current_price: 0,
  uc1: 0,
  uc2: 0,
  uc3: 0,
  uc4: 0,
  uc5: 0,
  uc6: 0,
  up1: 0,
  up2: 0,
  up3: 0,
  up4: 0,
  up5: 0,
  up6: 0,
  company: null,
  igic: false,
})
export default {
  name: 'Calculator',
  components: {
    ClientTypeSelect: () => import('~/components/selects/ClientTypeSelect'),
    TarifSelect: () => import('~/components/selects/TarifSelect'),
    CompanySelect: () => import('~/components/selects/CompanySelect'),
    SubmitButton: () => import('~/components/buttons/submitButton'),
    ReturnButton: () => import('~/components/buttons/returnButton'),
    CalculatorDetails: () => import('@/components/CalculatorDetails'),
    DecimalField: () => import('@/components/fields/decimalField'),
  },
  props: {
    hideOfferNames: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      hasReactiveEnergy: false,
      ourColor: constants.ourColor,
      errorMessages: {},
      loading: false,
      offer: null,
      showResults: false,
      form: { ...defaultForm },
    }
  },
  computed: {
    offers() {
      return this.$store.state.calculatedOffers
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
          text: 'Rank',
          value: 'ranking_price',
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
  watch: {
    form: {
      handler() {
        this.$store.dispatch('setCalculatorForm', { ...this.form })
      },
      deep: true,
    },
    'form.tarif'() {
      const fields = [
        ['p', 1],
        ['p', 2],
        ['p', 3],
        ['p', 4],
        ['p', 5],
        ['p', 6],
        ['c', 1],
        ['c', 2],
        ['c', 3],
        ['c', 4],
        ['c', 5],
        ['c', 6],
      ]
      fields.forEach((field) => {
        if (!this.showInput(field[0], field[1])) {
          delete this.form['u' + field[0] + field[1]]
        }
      })
    },
  },
  mounted() {
    this.form = { ...this.$store.state.calculatorForm }
  },
  methods: {
    resetForm() {
      this.form = { ...defaultForm }
    },
    showInput(letter, number) {
      return this.form.tarif && constants.showInput(letter, number, this.form.tarif)
    },
    submit() {
      this.errorMessages = {}
      this.loading = true
      const form = { ...this.form, reactive: this.hasReactiveEnergy ? this.reactive : 0 }
      const values = Object.fromEntries(
        Object.entries(form)
          .filter((i) => [undefined, null, ''].indexOf(i[1]) === -1)
          .filter((i) => {
            const key = i[0]
            if (key.startsWith('u') && key.length === 3) {
              return this.showInput(key[1], key[2]) ? true : false
            }
            if (key === 'reactive') {
              return this.hasReactiveEnergy ? true : false
            }
            return true
          })
          .map((item) => {
            const [key, val] = item
            if (typeof val === 'string' && val.includes(',')) {
              return [key, val.replaceAll(',', '.')]
            }
            return [key, val]
          }),
      )
      this.$axios
        .$post('calculator/calculate/', {
          ...values,
        })
        .then((data) => {
          this.$store.commit('setCalculatedOffers', data)
          this.showResults = true
        })
        .catch((e) => {
          if (e.response.status !== 400) this.$swal({ title: 'Error', text: String(e), icon: 'error' })
          if (e.response.data.error) {
            this.$swal({ title: 'Error', text: e.response.data.error, icon: 'error' })
          }
          this.errorMessages = e.response.data
        })
        .finally(() => (this.loading = false))
    },
  },
}
</script>
