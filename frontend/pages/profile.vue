<template>
  <v-card :loading="loading">
    <v-card-title>Perfil</v-card-title>
    <v-card-text>
      <v-form @submit.prevent="submit" novalidate>
        <v-card-text>
          <v-text-field
            prepend-icon="mdi-account"
            name="email"
            label="Email"
            type="text"
            v-model="form.email"
            :error-messages="error.email"
          ></v-text-field>
          <v-text-field
            prepend-icon="mdi-people"
            name="first_name"
            label="First name"
            type="text"
            v-model="form.first_name"
            :error-messages="error.first_name"
          ></v-text-field>
          <v-text-field
            prepend-icon="mdi-account"
            name="last_name"
            label="Last name"
            type="text"
            v-model="form.last_name"
            :error-messages="error.last_name"
          ></v-text-field>
          <v-text-field
            prepend-icon="mdi-phone"
            name="phone"
            label="Phone"
            type="tel"
            v-model="form.phone"
            :error-messages="error.phone"
          ></v-text-field>
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
export default {
  components: { SubmitButton },
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
        this.$swal({ title: 'Saved!', icon: 'success' })
      } catch (e) {
        this.error = e.response.data
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
