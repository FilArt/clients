<template>
  <v-card>
    <v-toolbar>
      <v-toolbar-title>Agregar nuevo punto</v-toolbar-title>

      <v-spacer />

      <v-toolbar-items>
        <v-btn color="error" nuxt to="/admin/ofertas">
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>

    <v-card-text>
      <v-row>
        <v-spacer />
        <v-col>
          <v-form @submit.prevent="submit">
            <v-text-field v-model="newOffer.name" label="Nombre" :error-messages="errorMessages.name" />

            <v-select
              v-model="newOffer.kind"
              label="Tipo"
              :items="['luz', 'gas']"
              :error-messages="errorMessages.kind"
            />
            <company-select v-model="newOffer.company" :error-messages="errorMessages.company" />
            <v-textarea
              v-model="newOffer.description"
              label="Description"
              :error-messages="errorMessages.description"
            />
            <tarif-select
              v-model="newOffer.tarif"
              :error-messages="errorMessages.tarif"
              :gas="newOffer.kind === 'gas'"
            />
            <client-type-select v-model="newOffer.client_type" :error-messages="errorMessages.client_type" />
            <decimal-field
              v-model="newOffer.power_min"
              label="Potencia min"
              :error-messages="errorMessages.power_min"
            />
            <decimal-field
              v-model="newOffer.power_max"
              label="Potencia max"
              :error-messages="errorMessages.power_max"
            />
            <decimal-field
              v-model="newOffer.consumption_min"
              label="Consumo min"
              :error-messages="errorMessages.consumption_min"
            />
            <decimal-field
              v-model="newOffer.consumption_max"
              label="Consumo max"
              :error-messages="errorMessages.consumption_max"
            />
            <decimal-field v-model="newOffer.p1" label="P1" :error-messages="errorMessages.p1" />
            <decimal-field v-model="newOffer.p2" label="P2" :error-messages="errorMessages.p2" />
            <decimal-field v-model="newOffer.p3" label="P3" :error-messages="errorMessages.p3" />
            <decimal-field v-model="newOffer.p4" label="P4" :error-messages="errorMessages.p4" />
            <decimal-field v-model="newOffer.p5" label="P5" :error-messages="errorMessages.p5" />
            <decimal-field v-model="newOffer.p6" label="P6" :error-messages="errorMessages.p6" />
            <decimal-field v-model="newOffer.c1" label="C1" :error-messages="errorMessages.c1" />
            <decimal-field v-model="newOffer.c2" label="C2" :error-messages="errorMessages.c2" />
            <decimal-field v-model="newOffer.c3" label="C3" :error-messages="errorMessages.c3" />
            <decimal-field v-model="newOffer.c4" label="C4" :error-messages="errorMessages.c4" />
            <decimal-field v-model="newOffer.c5" label="C5" :error-messages="errorMessages.c5" />
            <decimal-field v-model="newOffer.c6" label="C6" :error-messages="errorMessages.c6" />
            <v-select
              v-model="newOffer.is_price_permanent"
              label="Tipo de precio"
              :items="['Fijo', 'Indexado']"
              :error-messages="errorMessages.is_price_permanent"
            />
            <decimal-field
              v-model="newOffer.agent_commission"
              label="Agente comisiones"
              :error-messages="errorMessages.agent_commission"
            />
            <decimal-field
              v-model="newOffer.canal_commission"
              label="Canal comisiones"
              :error-messages="errorMessages.canal_commission"
            />
            <offer-required-fields
              v-model="newOffer.required_fields"
              :aria-errormessage="errorMessages.required_fields"
            />
            <v-btn :loading="loading" block type="submit" color="success">Enviar</v-btn>
          </v-form>
        </v-col>
        <v-spacer />
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
import CompanySelect from '@/components/selects/CompanySelect'
import TarifSelect from '@/components/selects/TarifSelect'
import ClientTypeSelect from '@/components/selects/ClientTypeSelect'
import OfferRequiredFields from '@/components/selects/OfferRequiredFields'
import DecimalField from '../../../components/fields/decimalField.vue'
const offerObject = {
  name: null,
  kind: null,
  company: null,
  tarif: null,
  power_min: null,
  power_max: null,
  consumption_min: null,
  consumption_max: null,
  client_type: null,
  p1: null,
  p2: null,
  p3: null,
  p4: null,
  p5: null,
  p6: null,
  c1: null,
  c2: null,
  c3: null,
  c4: null,
  c5: null,
  c6: null,
  is_price_permanent: null,
  canal_commission: null,
  agent_commission: null,
  required_fields: [],
}
export default {
  components: { OfferRequiredFields, ClientTypeSelect, TarifSelect, CompanySelect, DecimalField },
  data() {
    return {
      loading: false,
      newOffer: { ...offerObject },
      errorMessages: { ...offerObject },
    }
  },
  methods: {
    async submit() {
      this.loading = true
      const calculator = this.$route.query.comparador === 'true'
      try {
        await this.$axios.$post('/calculator/admin_offers/', { ...this.newOffer, calculator })
        await this.$router.push('/admin/ofertas_comparador')
      } catch (e) {
        this.errorMessages = e.response.data
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
