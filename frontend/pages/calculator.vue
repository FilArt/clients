<template>
  <v-card :loading="loading">
    <v-snackbar v-model="loading">
      <p>
        Считаем...
      </p>
      <v-progress-circular indeterminate />
    </v-snackbar>
    <v-list v-if="$route.query.showResults">
      <v-alert type="warning" :value="!offers.length">
        Offers not found
      </v-alert>

      <v-list-item
        v-for="offer in offers"
        :key="offer.id"
        nuxt
        :to="`offers/${offer.id}?back=${$route.fullPath}&fromCalculator=true`"
      >
        <v-list-item-avatar>
          <v-img :src="offer.company_logo || '/no-image.svg'" />
        </v-list-item-avatar>
        <v-list-item-title v-text="offer.name" />
        <v-list-item-subtitle v-text="offer.company" />
      </v-list-item>

      <v-list-item>
        <v-btn block nuxt to="/calculator">
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
        <company-select
          :value="form.company"
          :error-messages="errorMessages.company"
          @input="updateForm('company', $event)"
        />
        <tarif-select
          :value="form.tarif"
          :error-messages="errorMessages.tarif"
          @input="updateForm('tarif', $event)"
        />
        <v-text-field
          label="Periodo"
          :value="form.period"
          :error-messages="errorMessages.period"
          @input="updateForm('period', $event)"
        />
        <client-type-select
          :value="form.client_type"
          :error-messages="errorMessages.client_type"
          @input="updateForm('client_type', $event)"
        />
        <v-text-field
          label="C1"
          :value="form.c1"
          :error-messages="errorMessages.c1"
          @input="updateForm('c1', $event)"
        />
        <v-text-field
          label="C2"
          :value="form.c2"
          :error-messages="errorMessages.c2"
          @input="updateForm('c2', $event)"
        />
        <v-text-field
          label="C3"
          :value="form.c3"
          :error-messages="errorMessages.c3"
          @input="updateForm('c3', $event)"
        />
        <v-text-field
          label="P1"
          :value="form.p1"
          :error-messages="errorMessages.p1"
          @input="updateForm('p1', $event)"
        />
        <v-text-field
          label="P2"
          :value="form.p2"
          :error-messages="errorMessages.p2"
          @input="updateForm('p2', $event)"
        />
        <v-text-field
          label="P3"
          :value="form.p3"
          :error-messages="errorMessages.p3"
          @input="updateForm('p3', $event)"
        />
      </v-card-text>
      <v-card-actions>
        <submit-button block label="Calculate" @click="submit" />
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
    }
  },
  computed: {
    offers() {
      return this.$store.state.calculatedOffers
    },
    form() {
      return this.$store.state.calculatorForm
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
        .$post('calculator/calculate', this.form)
        .then((data) => {
          this.$store.commit('setCalculatedOffers', data)
          this.$router.replace({ query: { showResults: true } })
        })
        .catch((e) => (this.errorMessages = e.response.data))
        .finally(() => (this.loading = false))
    },
  },
}
</script>
