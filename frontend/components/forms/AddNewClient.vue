<template>
  <v-form novalidate @submit.prevent="submit">
    <v-text-field v-model="user.company_name" label="Nombre" :error-messages="errorMessages.company_name" />
    <email-field v-model="user.email" :error-messages="errorMessages.email" />
    <phone-field v-model="user.phone" :error-messages="errorMessages.phone" />

    <submit-button block label="Salvar" />
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
      },
      errorMessages: {},
    }
  },
  methods: {
    async submit() {
      this.errorMessages = {}
      const url = this.$auth.user.role === 'agent' ? 'users/new_client/' : 'users/manage_users/'
      try {
        const newClient = await this.$axios.$post(url, this.user)
        this.$emit('added', newClient)
      } catch (e) {
        this.errorMessages = e.response.data
      }
    },
  },
}
</script>
