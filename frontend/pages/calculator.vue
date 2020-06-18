<template>
  <v-card :loading="loading">
    <v-snackbar v-model="loading">
      <p>
        Считаем...
      </p>
      <v-progress-circular indeterminate />
    </v-snackbar>
    <v-list v-if="showResults">
      <v-alert type="warning" :value="!offers.length">
        Offers not found
      </v-alert>

      <v-list-item
        v-for="offer in offers"
        :key="offer.id"
        nuxt
        :to="`offers/${offer.id}?id=${offer.id}&back=${$route.fullPath}&fromCalculator=true`"
      >
        <v-list-item-avatar>
          <v-img :src="offer.company_logo || '/no-image.svg'" />
        </v-list-item-avatar>
        <v-list-item-title v-text="offer.name" />
        <v-list-item-subtitle v-text="offer.company" />
      </v-list-item>

      <v-list-item>
        <v-btn block @click="showResults = false">
          Вернуться к расчетам
          <v-icon>mdi-keyboard-return</v-icon>
        </v-btn>
      </v-list-item>
    </v-list>
    <v-form v-else @submit.prevent="submit" novalidate>
      <v-card-title>
        Comparador
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col>
            <company-select
              :value="form.company"
              :error-messages="errorMessages.company"
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

        <v-text-field
          label="Periodo"
          :value="form.period"
          :error-messages="errorMessages.period"
          @input="updateForm('period', $event)"
        />

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
                  :value="form[letter + number]"
                  :label="letter.toUpperCase() + number"
                  :error-messages="errorMessages[letter + number]"
                  @input="updateForm(letter + number, $event)"
                />
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <submit-button block label="Calculate" />
      </v-card-actions>
    </v-form>
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
