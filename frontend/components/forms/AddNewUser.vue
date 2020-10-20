<template>
  <v-dialog v-model="dialog" max-width="750">
    <template v-slot:activator="{ on }">
      <v-btn icon color="success" v-on="on">
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </template>
    <v-card>
      <v-card-title>
        Añadir nuevo cliente
        <v-spacer />
        <close-button @click="dialog = false" />
      </v-card-title>

      <v-card-text>
        <v-form novalidate @submit.prevent="submit">
          <v-text-field v-model="user.company_name" label="Nombre" :error-messages="errorMessages.company_name" />
          <email-field v-model="user.email" :error-messages="errorMessages.email" />
          <phone-field v-model="user.phone" :error-messages="errorMessages.phone" />
          <submit-button block label="Salvar" />
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import CloseButton from '@/components/buttons/closeButton'
import PhoneField from '@/components/fields/phoneField'
import EmailField from '@/components/fields/emailField'
import SubmitButton from '@/components/buttons/submitButton'

export default {
  name: 'AddNewClient',
  components: { SubmitButton, EmailField, PhoneField, CloseButton },
  data() {
    return {
      dialog: false,
      user: {
        company_name: null,
        email: null,
        role: null,
      },
      errorMessages: {},
    }
  },
  methods: {
    async submit() {
      this.errorMessages = {}
      try {
        await this.$axios.$post('users/manage_users/', this.user)
        this.$emit('added')
        this.dialog = false
      } catch (e) {
        this.errorMessages = e.response.data
      }
    },
  },
}
</script>
