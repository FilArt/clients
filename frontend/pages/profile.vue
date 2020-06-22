<template>
  <v-card :loading="loading">
    <v-card-title>Perfil</v-card-title>
    <v-card-text>
      <v-form @submit.prevent="submit" novalidate>
        <v-card-text>
          <email-field v-model="form.email" :error-messages="error.email" />
          <v-text-field
            v-model="form.first_name"
            label="First name"
            name="first_name"
            prepend-icon="mdi-account-box"
            type="text"
            :error-messages="error.first_name"
          />
          <v-text-field
            v-model="form.last_name"
            label="Last name"
            name="last_name"
            prepend-icon="mdi-account-box"
            type="text"
            :error-messages="error.last_name"
          />
          <phone-field v-model="form.phone" :error-messages="error.phone" />
        </v-card-text>
        <v-card-actions>
          <submit-button block label="Save" />
        </v-card-actions>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
import SubmitButton from '~/components/buttons/submitButton'
import PhoneField from '~/components/fields/phoneField'
import EmailField from '~/components/fields/emailField'
export default {
  components: { EmailField, PhoneField, SubmitButton },
  data() {
    return {
      error: {},
      loading: false,
      form: {
        email: this.$auth.user.email,
        first_name: this.$auth.user.first_name,
        last_name: this.$auth.user.last_name,
        phone: this.$auth.user.phone,
      },
    }
  },
  methods: {
    async submit() {
      this.loading = true
      this.error = {}
      try {
        this.form = await this.$axios.$patch(
          `users/account/${this.$auth.user.id}/`,
          this.form
        )
        this.$swal({ title: 'Salvado', icon: 'success' })
      } catch (e) {
        this.error = e.response.data
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
