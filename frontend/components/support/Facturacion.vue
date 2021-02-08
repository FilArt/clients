<template>
  <v-row align="center">
    <v-col>
      <v-row>
        <v-col>
          <v-toolbar>Responsable: {{ responsible }}</v-toolbar>

          <v-radio-group
            :value="responsibleCommission"
            label="Responsable comisiones"
            @change="pagar('commission', $event)"
          >
            <v-radio :value="defaultResponsibleCommission" :label="`${defaultResponsibleCommission} €`" />
            <v-text-field
              v-model="responsibleCommission"
              label="Variable"
              append-icon="mdi-content-save"
              prepend-icon="mdi-currency-eur"
              @click:append="pagar('commission', responsibleCommission)"
            />
          </v-radio-group>
        </v-col>
      </v-row>

      <v-row v-if="canal" align="center">
        <v-col>
          <v-toolbar>Canal: {{ canal }}</v-toolbar>

          <v-radio-group :value="canalCommission" label="Canal comisiones" @change="pagar('canal_commission', $event)">
            <v-radio :value="defaultCanalCommission" :label="`${defaultCanalCommission} €`" />
            <v-text-field
              v-model="canalCommission"
              label="Variable"
              append-icon="mdi-content-save"
              prepend-icon="mdi-currency-eur"
              @click:append="pagar('canal_commission', canalCommission)"
            />
          </v-radio-group>
        </v-col>
      </v-row>
    </v-col>

    <v-col>
      <v-row>
        <v-col>
          <v-radio-group
            v-model="responsiblePaid"
            :error-messages="errorMessages.paid"
            @change="pagar('paid', responsiblePaid)"
          >
            <v-radio label="Pagado" :value="true" color="success" />
            <v-radio label="Pendiente" :value="false" color="error" />
          </v-radio-group>
        </v-col>
      </v-row>

      <v-row v-if="canal">
        <v-col>
          <v-radio-group
            v-model="canalPaid"
            :error-messages="errorMessages.canal_paid"
            @change="pagar('canal_paid', canalPaid)"
          >
            <v-radio label="Pagado" :value="true" color="success" />
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
    bidId: {
      type: [Number, String],
      default: 0,
    },
    canal: {
      type: String,
      default: '',
    },
    responsible: {
      type: String,
      default: '',
    },
    defaultResponsibleCommission: {
      type: Number,
      default: 0,
    },
    defaultCanalCommission: {
      type: Number,
      default: 0,
    },
    currentResponsibleCommission: {
      type: Number,
      default: 0,
    },
    currentCanalCommission: {
      type: Number,
      default: 0,
    },
    isResponsiblePaid: {
      type: Boolean,
      default: false,
    },
    isCanalPaid: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      responsibleCommission: this.currentResponsibleCommission,
      canalCommission: this.currentCanalCommission,
      responsiblePaid: this.isResponsiblePaid,
      canalPaid: this.isCanalPaid,
      errorMessages: {
        paid: null,
        canal_paid: null,
      },
    }
  },
  methods: {
    async pagar(field, value) {
      if (field === 'commission') this.responsibleCommission = value
      if (field === 'canal_commission') this.canalCommission = value
      this.errorMessages = {}
      try {
        this.bid = await this.$axios.$patch(`bids/bids/${this.bidId}/`, { [field]: value })
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
