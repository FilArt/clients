<template>
  <v-row align="center">
    <v-col>
      <v-row>
        <v-col>
          <v-toolbar>Responsable: {{ bid.responsible }}</v-toolbar>

          <v-radio-group
            :value="wallet.responsible.commission"
            label="Responsable comisiones"
            @change="pagar('commission', $event)"
          >
            <v-radio :value="bid.offer.agent_commission" :label="`${bid.offer.agent_commission} €`" />
            <v-text-field
              v-model="wallet.responsible.commission"
              label="Variable"
              append-icon="mdi-content-save"
              prepend-icon="mdi-currency-eur"
              @click:append="pagar('commission', wallet.responsible.commission)"
            />
          </v-radio-group>
        </v-col>
      </v-row>

      <v-row v-if="bid.canal" align="center">
        <v-col>
          <v-toolbar>Canal: {{ bid.canal }}</v-toolbar>

          <v-radio-group
            :value="wallet.canal.commission"
            label="Canal comisiones"
            @change="pagar('canal_commission', $event)"
          >
            <v-radio :value="bid.offer.canal_commission" :label="`${bid.offer.canal_commission} €`" />
            <v-text-field
              v-model="wallet.canal.commission"
              label="Variable"
              append-icon="mdi-content-save"
              prepend-icon="mdi-currency-eur"
              @click:append="pagar('canal_commission', wallet.canal.commission)"
            />
          </v-radio-group>
        </v-col>
      </v-row>
    </v-col>

    <v-col>
      <v-row>
        <v-col>
          <v-radio-group
            v-model="wallet.responsible.paid"
            :error-messages="errorMessages.paid"
            @change="pagar('paid', wallet.responsible.paid)"
          >
            <v-radio :label="`Pagado ${wallet.responsible.commission}`" :value="true" color="success" />
            <v-radio label="Pendiente" :value="false" color="error" />
          </v-radio-group>
        </v-col>
      </v-row>

      <v-row v-if="bid.canal">
        <v-col>
          <v-radio-group
            v-model="wallet.canal.paid"
            :error-messages="errorMessages.canal_paid"
            @change="pagar('canal_paid', wallet.canal.paid)"
          >
            <v-radio :label="`Pagado ${wallet.canal.commission}`" :value="true" color="success" />
            <v-radio label="Pendiente" :value="false" color="error" />
          </v-radio-group>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'Facturacion',
  props: {
    bid: {
      type: Object,
      default: () => ({}),
    },
  },
  data() {
    return {
      errorMessages: {
        paid: null,
        canal_paid: null,
      },
      wallet: {
        responsible: {
          commission: this.bid.commission,
          paid: this.bid.paid,
        },
        canal: {
          commission: this.bid.canal_commission,
          paid: this.bid.canal_paid,
        },
      },
    }
  },
  methods: {
    async pagar(field, value) {
      if (field === 'commission') this.wallet.responsible.commission = value
      if (field === 'canal_commission') this.wallet.canal.commission = value
      this.errorMessages = {}
      try {
        await this.$axios.$patch(`bids/bids/${this.bid.id}/`, { [field]: value })
        this.$toast.global.done()
        this.$emit('paid')
      } catch (e) {
        const err = e.response.data
        if (err.detail) {
          await this.$swal({ title: 'Error', text: err.detail, icon: 'error' })
        }
        this.errorMessages = err
      }
    },
  },
}
</script>
