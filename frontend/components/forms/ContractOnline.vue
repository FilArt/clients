<template>
  <v-card flat>
    <div v-if="withFactura" class="text-center" style="font-size: 42px; color: #004680;">
      No encuentras los datos solicitados?
    </div>

    <div v-else class="text-center" style="font-size: 30px; color: #004680;">
      {{ showAdditionalFields ? 'Contratar online' : 'Contractar con asistente personal' }}
    </div>

    <div v-if="withFactura" class="pa-5 text-center" style="color: #004680;">
      Envianos un duplicado o foto de su factura y uno de nuestros agentes especializados le enviara el estudio
      detallando toda la informacion sobre su estado acual y propuesta de ahorro.
    </div>

    <v-row>
      <v-spacer />
      <v-col>
        <v-form class="mx-auto" style="max-width: 500px;" @submit.prevent="submit">
          <v-text-field v-model="user.first_name" autofocus label="Nombre" :error-messages="errorMessages.first_name" />
          <phone-field v-model="user.phone" :error-messages="errorMessages.phone" />
          <email-field v-model="user.email" :error-messages="errorMessages.email" />

          <v-file-input
            v-if="showAdditionalFields || withFactura"
            v-model="user.factura"
            label="Foto factura actual (anverso)"
            accept="image/*"
            :error-messages="errorMessages.factura"
          />

          <v-file-input
            v-if="showAdditionalFields || withFactura"
            v-model="user.factura_1"
            label="Foto factura actual (reverso)"
            accept="image/*"
            :error-messages="errorMessages.factura_1"
          />

          <v-file-input
            v-if="showAdditionalFields"
            v-model="user.dni1"
            label="Foto DNI (anverso)"
            accept="image/*"
            :error-messages="errorMessages.dni1"
          />

          <v-file-input
            v-if="showAdditionalFields"
            v-model="user.dni2"
            label="Foto DNI (reverso)"
            accept="image/*"
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
      </v-col>
      <v-spacer />
    </v-row>
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
    withFactura: {
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
      const aep = `contract_online${this.showAdditionalFields ? '_plus' : this.withFactura ? '_with_factura' : ''}`
      const postData = this.withFactura ? { ...this.user } : { ...this.user, offer: this.offer.id }
      const formData = new FormData()
      for (const field in postData) {
        const value = postData[field]
        if (value !== null) formData.append(field, value)
      }
      try {
        await this.$axios.$post(`users/${aep}/`, formData)
        location.replace('https://gestiongroup.es/gracias-por-registrarte-comparador')
      } catch (e) {
        this.errorMessages = e.response.data
      }
    },
  },
}
</script>
