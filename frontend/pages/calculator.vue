<template>
  <v-card :loading="loading">
    <v-card-text class="text-center">
      <div class="text-h4">
        Utiliza nuestra herramienta de selección de ofertas.
      </div>

      <div class="text-h6">
        Para utilizar el comparador, necesitará su factura de luz actual.
        Nuestro comparador realizará un cálculo para todas las ofertas
        disponibles en nuestra base de datos y lo ayudará a elegir la mejor
        oferta para usted.
      </div>
    </v-card-text>

    <v-simple-table v-if="showResults">
      <v-alert type="warning" :value="!offers.length">Nohay ofertas</v-alert>

      <template v-slot:default>
        <thead>
          <tr>
            <th></th>
            <th>Oferta</th>
            <th>Comercializadora</th>
            <th>Ahorro en factura</th>
            <th>Ahorro anual</th>
            <th></th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="offer in offers" :key="offer.id">
            <td>
              <v-list-item-avatar>
                <v-img :src="offer.company_logo || '/no-image.svg'" />
              </v-list-item-avatar>
            </td>
            <td>{{ offer.name }}</td>
            <td>{{ offer.company_name }}</td>
            <td>{{ offer.total }} €</td>
            <td>{{ offer.annual_total }} €</td>
            <td>
              <v-btn
                icon
                nuxt
                :to="`/offers/detail/${offer.id}?id=${offer.id}&showCalculatorDetails=true`"
              >
                <v-icon>mdi-eye</v-icon>
              </v-btn>
            </td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>

    <div v-else>
      <v-form @submit.prevent="submit" novalidate>
        <v-card-text class="mx-auto" style="max-width: 1000px;">
          <v-row align="center" class="flex-wrap">
            <v-col>
              <company-select
                :value="form.company"
                :error-messages="errorMessages.company"
                label="Comercializadora actual"
                @input="updateForm('company', $event)"
              />
            </v-col>

            <v-col>
              <tarif-select
                :value="tarif"
                :error-messages="errorMessages.tarif"
                @input="$store.commit('setTarif', $event)"
              />
            </v-col>

            <v-col>
              <client-type-select
                :value="form.client_type"
                :error-messages="errorMessages.client_type"
                @input="updateForm('client_type', $event)"
              />
            </v-col>
          </v-row>

          <v-row>
            <v-col>
              <v-text-field
                label="Periodo"
                type="number"
                name="period"
                hint="En este campo, ingrese el período (en días) por el cual se le factura. Está información puede obtenerse en su factura."
                persistent-hint
                :value="form.period"
                :error-messages="errorMessages.period"
                @input="updateForm('period', $event)"
              />
            </v-col>

            <v-col>
              <v-text-field
                label="Cadidad de pago en la factura actual"
                type="number"
                name="current_price"
                prefix="€"
                :value="form.current_price"
                :error-messages="errorMessages.current_price"
                @input="updateForm('current_price', $event)"
              />
            </v-col>
          </v-row>

          <v-row>
            <v-col v-for="letter in ['p', 'c']" :key="letter">
              <v-row v-for="number in [1, 2, 3]" :key="number">
                <v-col>
                  <v-text-field
                    v-show="
                      number === 1 ||
                      ['3.0A', '3.1A'].includes(tarif) ||
                      (letter + number === 'c3' &&
                        ['2.1DHA', '2.0DHA'].includes(tarif))
                    "
                    type="number"
                    :hint="
                      letter === 'p'
                        ? 'Ingrese aquí la potencia contratada en kw. Está información puede obtenerse en su factura'
                        : 'Ingrese aquí la energía consumida en kw para cada período.Está información puede obtenerse en su factura.'
                    "
                    persistent-hint
                    :value="form[letter + number]"
                    :label="
                      (letter === 'p' ? 'Potencia' : 'Consumo') + ' P' + number
                    "
                    :name="'P' + number"
                    :error-messages="errorMessages[letter + number]"
                    @input="updateForm(letter + number, $event)"
                  />
                </v-col>
              </v-row>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <submit-button block label="Comparar" />
        </v-card-actions>
      </v-form>
    </div>
  </v-card>
</template>
<script>
export default {
  components: {
    ClientTypeSelect: () => import('~/components/selects/ClientTypeSelect'),
    TarifSelect: () => import('~/components/selects/TarifSelect'),
    CompanySelect: () => import('~/components/selects/CompanySelect'),
    SubmitButton: () => import('~/components/buttons/submitButton'),
  },
  data() {
    return {
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
    tarif() {
      return this.$store.state.tarif
    },
  },
  methods: {
    updateForm(key, value) {
      this.$store.commit('updateCalculatorForm', {
        key: key,
        value: value,
      })
    },
    submit() {
      this.errorMessages = {}
      this.loading = true
      this.$axios
        .$post('calculator/calculate', { tarif: this.tarif, ...this.form })
        .then((data) => {
          this.$store.commit('setCalculatedOffers', data)
          this.showResults = true
        })
        .catch((e) => (this.errorMessages = e.response.data))
        .finally(() => (this.loading = false))
    },
  },
}
</script>
