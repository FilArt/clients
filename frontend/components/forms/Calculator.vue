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
      <template v-slot:[`item.annual_profit_num`]="{ item }"> {{ item.annual_profit_num }} € </template>

      <template v-slot:[`item.actions`]="{ item }">
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
                updateForm('tarif', null)
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
                updateForm('tarif', null)
              "
            >
              <v-card-title>Gas</v-card-title><v-icon large color="red" right>mdi-fire</v-icon>
            </v-btn>
          </v-card>

          <v-row align="center" class="text-center">
            <v-col>
              Impuestos
              <v-btn-toggle
                mandatory
                :value="form.igic || false"
                :color="ourColor"
                @change="updateForm('igic', $event)"
              >
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
                :value="form.client_type"
                :error-messages="errorMessages.client_type"
                hint
                without-autonomo
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
              <tarif-select
                v-model="tarif"
                :error-messages="errorMessages.tarif"
                hint
                :gas="form.kind === 'gas'"
                @input="updateForm('tarif', tarif)"
              />
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

          <v-row v-if="form.kind === 'luz'" align="center">
            <v-col>
              <v-checkbox
                v-model="hasReactiveEnergy"
                label="Energía reactiva (opcional)"
                @change="!$event ? updateForm('reactive', 0) : null"
              />
            </v-col>

            <v-col>
              <v-text-field
                v-show="hasReactiveEnergy"
                prefix="€"
                label="Cadidad de pago energía reactiva"
                :value="form.reactive"
                :error-messages="errorMessages.reactive"
                @input="updateForm('reactive', $event && $event.length ? $event : null)"
              />
            </v-col>
          </v-row>

          <v-row>
            <submit-button :disabled="hasReactiveEnergy ? !form.reactive : false" block label="Comparar" />
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
    detailUrl: {
      type: String,
      default: null,
    },
  },
  data() {
    return {
      hasReactiveEnergy: false,
      ourColor: constants.ourColor,
      errorMessages: {},
      loading: false,
      showResults: false,
      tarif: null,
    }
  },
  computed: {
    offers() {
      return this.$store.state.calculatedOffers
    },
    form() {
      return this.$store.state.calculatorForm
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
          value: 'annual_profit_num',
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
    tarif() {
      this.updateForm('tarif', this.tarif)
      const fields = [
        ['p', 2],
        ['p', 3],
        ['c', 2],
        ['c', 3],
      ]
      fields.forEach((field) => {
        if (!this.showInput(field[0], field[1])) {
          this.updateForm(field[0] + field[1], null)
        }
      })
    },
  },
  mounted() {
    this.$store.commit('resetCalculator')
  },
  methods: {
    getDetailUrl(offer) {
      return this.detailUrl
        ? this.detailUrl.replace('place_for_id', String(offer.id))
        : `/ofertas/${offer.client_type === 0 ? 'hogar' : 'pyme'}/${offer.id}/?id=${
            offer.id
          }&showCalculatorDetails=true`
    },
    showInput(letter, number) {
      return constants.showInput(letter, number, this.tarif)
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
        .$post('calculator/calculate/', {
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
