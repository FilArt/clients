<template>
  <v-dialog v-model="dialog" max-width="750">
    <template v-slot:activator="{ on }">
      <v-btn icon v-on="on">
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </template>
    <v-card>
      <v-card-title>
        Añadir nuevo empleado
        <v-spacer />
        <close-button @click="dialog = false" />
      </v-card-title>

      <v-card-text>
        <v-form novalidate @submit.prevent="submit">
          <v-text-field v-model="user.first_name" label="Nombre" :error-messages="errorMessages.first_name" />
          <v-text-field v-model="user.last_name" label="Apellido" :error-messages="errorMessages.last_name" />
          <email-field v-model="user.email" :error-messages="errorMessages.email" />
          <phone-field v-model="user.phone" :error-messages="errorMessages.phone" />
          <v-select
            v-model="user.role"
            label="Role"
            :items="[
              { text: 'Admin', value: 'admin' },
              { text: 'Agente', value: 'agent' },
              { text: 'Tramitación', value: 'support' },
            ]"
            :error-messages="errorMessages.role"
          />
          <submit-button block label="Guardar" />
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
  name: 'AddNewEmployee',
  components: { SubmitButton, EmailField, PhoneField, CloseButton },
  data() {
    return {
      dialog: false,
      user: {},
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
