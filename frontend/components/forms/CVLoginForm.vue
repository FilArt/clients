<template>
  <v-dialog v-model="dialog">
    <template v-slot:activator="{ on }">
      <v-btn color="success" v-on="on"> Login to Call&Visit </v-btn>
    </template>
    <v-card :loading="loading">
      <v-card-title> Call&Visit login </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="submit">
          <email-field v-model="form.email" :error-messages="error.email" />
          <v-text-field v-model="form.password" label="Password" />
          <submit-button />
        </v-form>
      </v-card-text>

      <v-card-text v-if="error.non_field_errors">
        <v-alert color="error">
          {{ error.non_field_errors[0] }}
        </v-alert>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import EmailField from '~/components/fields/emailField'
import SubmitButton from '~/components/buttons/submitButton'
export default {
  name: 'CVLoginForm',
  components: { SubmitButton, EmailField },
  data() {
    return {
      dialog: false,
      form: {
        email: null,
        password: null,
      },
      loading: false,
      error: {},
    }
  },
  methods: {
    async submit() {
      this.error = {}
      this.loading = true
      try {
        await this.$axios.$post('/cv_integration/', this.form)
        this.$emit('done')
        this.dialog = false
      } catch (e) {
        this.error = e.response.data
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
