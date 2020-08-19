<template>
  <v-card :loading="loading">
    <v-card-text class="text-center">
      <div class="text-h4">
        Perfil
      </div>
    </v-card-text>
    <v-card-text>
      <v-form novalidate @submit.prevent="submit">
        <v-card-text>
          <email-field v-model="form.email" :error-messages="error.email" />
          <v-text-field
            v-model="form.first_name"
            label="Nombre"
            name="first_name"
            prepend-icon="mdi-account-box"
            type="text"
            :error-messages="error.first_name"
          />
          <v-text-field
            v-model="form.last_name"
            label="Apellidos"
            name="last_name"
            prepend-icon="mdi-account-box"
            type="text"
            :error-messages="error.last_name"
          />
          <phone-field v-model="form.phone" />
        </v-card-text>
        <v-card-actions>
          <submit-button block label="Guardar" />
        </v-card-actions>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  components: {
    PhoneField: () => import('@/components/fields/phoneField'),
    EmailField: () => import('~/components/fields/emailField'),
    SubmitButton: () => import('~/components/buttons/submitButton'),
  },
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
      this.form.phone = this.form.phone ? this.form.phone.replace(' ', '') : null
      try {
        this.form = await this.$axios.$patch(`users/account/${this.$auth.user.id}/`, this.form)
        await this.$auth.fetchUser()
        await this.$swal({ title: 'Salvado', icon: 'success' })
      } catch (e) {
        this.error = e.response.data
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
