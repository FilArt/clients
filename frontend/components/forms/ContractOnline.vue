<template>
  <v-card>
    <v-card-title>
      {{ showAdditionalFields ? 'Contratar online' : 'Contractar con asistente personal' }}
    </v-card-title>

    <v-card-text>
      <v-form @submit.prevent="submit">
        <v-text-field v-model="user.first_name" autofocus label="Nombre" :error-messages="errorMessages.first_name" />
        <phone-field v-model="user.phone" :error-messages="errorMessages.phone" />
        <email-field v-model="user.email" :error-messages="errorMessages.email" />

        <v-file-input
          v-if="showAdditionalFields"
          v-model="user.factura"
          label="Foto factura actual (anverso)"
          :error-messages="errorMessages.factura"
        />

        <v-file-input
          v-if="showAdditionalFields"
          v-model="user.factura_1"
          label="Foto factura actual (reverso)"
          :error-messages="errorMessages.factura_1"
        />

        <v-file-input
          v-if="showAdditionalFields"
          v-model="user.dni1"
          label="Foto DNI (anverso)"
          :error-messages="errorMessages.dni1"
        />

        <v-file-input
          v-if="showAdditionalFields"
          v-model="user.dni2"
          label="Foto DNI (reverso)"
          :error-messages="errorMessages.dni2"
        />

        <v-text-field
          v-if="showAdditionalFields"
          v-model="user.iban"
          label="IBAN"
          :error-messages="errorMessages.iban"
        />

        <privacy />

        <submit-button label="Contractar" block :loading="loading" :disabled="!$store.state.privacyAccepted" />
      </v-form>
    </v-card-text>
  </v-card>
</template>
<script>
import Privacy from '~/components/other/Privacy'
import submitButton from '~/components/buttons/submitButton'
import phoneField from '~/components/fields/phoneField'
import emailField from '~/components/fields/emailField'
export default {
  name: 'ContractOnline',
  components: {
    Privacy,
    submitButton,
    phoneField,
    emailField,
  },
  props: {
    showAdditionalFields: {
      type: Boolean,
      default: false,
    },
    offer: {
      type: Object,
      default: () => {
        return {}
      },
    },
    calculations: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      loading: true,
      user: {
        first_name: '',
        email: '',
        phone: '',
        factura: null,
        factura_1: null,
        dni1: null,
        dni2: null,
        iban: null,
      },
      errorMessages: {
        first_name: null,
        email: null,
        phone: null,
        factura: null,
        factura_1: null,
        dni1: null,
        dni2: null,
        iban: null,
      },
    }
  },
  methods: {
    async submit() {
      const aep = this.showAdditionalFields ? 'contract_online_plus' : 'contract_online'
      const postData = { ...this.user, offer: this.offer.id }
      const formData = new FormData()
      for (const field in postData) {
        const value = postData[field]
        formData.append(field, value)
      }
      try {
        await this.$axios.$post(`users/${aep}/`, formData)
        location.replace('https://gestiongroup.es/gracias-por-registrarte')
      } catch (e) {
        this.errorMessages = e.response.data
      }
    },
  },
}
</script>
