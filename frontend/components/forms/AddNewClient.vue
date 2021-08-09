<template>
  <v-form novalidate @submit.prevent="submit">
    <v-text-field v-model="user.cif_nif" label="CIF/NIF" :error-messages="errorMessages.cif_nif" />
    <email-field v-model="user.email" :error-messages="errorMessages.email" />
    <phone-field v-model="user.phone" :error-messages="errorMessages.phone" />
    <v-text-field v-model="user.company_name" label="Nombre" :error-messages="errorMessages.company_name" />
    <v-text-field
      v-model="user.legal_representative"
      label="Persona de contacto"
      :error-messages="errorMessages.legal_representative"
    />
    <v-textarea v-model="user.observations" label="Observaciones" :error-messages="errorMessages.observations" />

    <submit-button block label="Guardar" />
  </v-form>
</template>

<script>
import PhoneField from '@/components/fields/phoneField'
import EmailField from '@/components/fields/emailField'
import SubmitButton from '@/components/buttons/submitButton'

export default {
  name: 'AddNewClient',
  components: { SubmitButton, EmailField, PhoneField },
  data() {
    return {
      user: {
        company_name: null,
        email: null,
        phone: null,
        cif_nif: null,
        legal_representative: null,
        observations: null,
      },
      errorMessages: {},
    }
  },
  methods: {
    async submit() {
      console.log(this)
      this.errorMessages = {}
      const url = this.$auth.user.role === 'agent' ? 'users/new_client/' : 'users/manage_users/'
      try {
        const { id } = await this.$axios.$post(url, this.user)
        const { role } = this.$auth.user
        this.$router.push(`/${role}/tramitacion/${id}`)
      } catch (e) {
        if (e && e.response && e.response.data) {
          this.errorMessages = e.response.data
        } else {
          this.$toasted.error(JSON.stringify(e))
        }
      }
    },
  },
}
</script>
