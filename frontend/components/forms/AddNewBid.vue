<template>
  <v-card>
    <v-toolbar>
      <v-toolbar-title class="flex-grow-1">Añadir nuevo solicitud</v-toolbar-title>

      <v-toolbar-items>
        <v-btn color="error" icon @click="$emit('close')">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>

    <v-form @submit.prevent="submit">
      <v-card-text>
        <company-select v-model="company" />
        <tarif-select v-model="tarif" all />
        <client-type-select v-model="clientType" />
      </v-card-text>

      <v-card-text>
        <offer-select v-model="offer" :tarif="tarif" :company="company" :client-type="clientType" />
      </v-card-text>

      <v-card-text>
        <v-card-title> Elejir punto </v-card-title>
        <v-row>
          <v-col>
            <v-btn
              v-for="p in puntos"
              :key="p.id"
              :color="punto && punto.id === p.id ? 'success' : null"
              @click="punto = p"
            >
              {{ p.id }}. {{ p.cups_luz || p.cups_gas }}
            </v-btn>
          </v-col>
        </v-row>

        <submit-button
          v-if="punto && offer"
          :label="`Salvar nuevo solicitud con punto ${punto.id} y oferta ''${offer.name}''`"
        />
      </v-card-text>

      <v-divider />

      <v-card-text>
        <add-punto v-if="offer" :bid="{ offer }" :user-id="userId" @punto-added="$emit('bid-added')" />
      </v-card-text>
    </v-form>
  </v-card>
</template>

<script>
export default {
  name: 'AddNewBid',
  components: {
    SubmitButton: () => import('@/components/buttons/submitButton'),
    AddPunto: () => import('@/components/puntos/AddPunto'),
    OfferSelect: () => import('@/components/selects/OfferSelect'),
    ClientTypeSelect: () => import('@/components/selects/ClientTypeSelect'),
    TarifSelect: () => import('@/components/selects/TarifSelect'),
    CompanySelect: () => import('@/components/selects/CompanySelect'),
  },
  props: {
    userId: {
      type: Number,
      default: null,
    },
  },
  data() {
    return {
      company: null,
      tarif: null,
      clientType: null,
      offer: null,
      punto: null,
      puntos: [],
    }
  },
  async mounted() {
    this.puntos = await this.$axios.$get(`/users/puntos/?user=${this.userId}`)
  },
  methods: {
    async submit() {
      try {
        await this.$axios.$post('bids/bids/', { user: this.userId, offer: this.offer.id, punto: this.punto.id })
        this.$emit('bid-added')
      } catch (e) {
        console.error(e)
        await this.$swal({ title: 'Error', text: e.response.data, icon: 'error' })
      }
    },
  },
}
</script>
