<template>
  <v-card>
    <v-form @submit.prevent="submit" novalidate>
      <v-card-title>
        Calculator
      </v-card-title>
      <v-card-text>
        <company-select
          v-model="form.company"
          :error-messages="errorMessages.company"
        />
        <tarif-select
          v-model="form.tarif"
          :error-messages="errorMessages.tarif"
        />
        <v-text-field
          v-model="form.period"
          label="Period"
          :error-messages="errorMessages.period"
        />
        <v-text-field
          v-model="form.power"
          label="Power"
          :error-messages="errorMessages.power"
        />
        <v-text-field
          v-model="form.annual_consumption"
          label="Annual consumption"
          :error-messages="errorMessages.annual_consumption"
        />
        <v-text-field
          v-model="form.client_type"
          label="Client type"
          :error-messages="errorMessages.client_type"
        />
        <v-text-field
          v-model="form.c1"
          label="C1"
          :error-messages="errorMessages.c1"
        />
        <v-text-field
          v-model="form.c2"
          label="C2"
          :error-messages="errorMessages.c2"
        />
        <v-text-field
          v-model="form.c3"
          label="C3"
          :error-messages="errorMessages.c3"
        />
        <v-text-field
          v-model="form.p1"
          label="P1"
          :error-messages="errorMessages.p1"
        />
        <v-text-field
          v-model="form.p2"
          label="P2"
          :error-messages="errorMessages.p2"
        />
        <v-text-field
          v-model="form.p3"
          label="P3"
          :error-messages="errorMessages.p3"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <submit-button @click="submit" />
      </v-card-actions>
    </v-form>
  </v-card>
</template>
<script>
import SubmitButton from '~/components/buttons/submitButton'
import CompanySelect from '~/components/selects/CompanySelect'
import TarifSelect from '~/components/selects/TarifSelect'
export default {
  components: { TarifSelect, CompanySelect, SubmitButton },
  data() {
    return {
      errorMessages: {},

      form: {
        company: null,
        tarif: null,
        period: 0,
        power: 0,
        annual_consumption: 0,
        client_type: 0,
        c1: 0,
        c2: 0,
        c3: 0,
        p1: 0,
        p2: 0,
        p3: 0
      }
    }
  },
  methods: {
    submit() {
      this.errorMessages = {}
      this.$axios
        .$post('calculator/calculate', this.form)
        .then(data => {
          this.$swal({
            title: 'Results ',
            icon: 'success',
            text: JSON.stringify(data)
          })
        })
        .catch(e => (this.errorMessages = e.response.data))
    }
  }
}
</script>
