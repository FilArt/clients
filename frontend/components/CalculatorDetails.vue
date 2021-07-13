<template>
  <v-card elevation="0">
    <v-card-actions>
      <v-spacer />

      <v-btn style="margin-right: 7em" color="success" :disabled="loading || downloading" rounded @click="getDetails">
        <v-icon>mdi-refresh</v-icon>
      </v-btn>

      <v-dialog v-model="rewriteValuesFormDialog" max-width="750" scrollable>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on"> Cambiar valores </v-btn>
        </template>
        <v-card>
          <v-card-text>
            <v-card flat class="d-flex flex-wrap">
              <v-card v-for="field in rewriteValuesForm" :key="field.name" class="mb-6 pa-2" flat>
                <div v-if="field.items && field.items.length">
                  <v-select
                    v-model="newTax.key"
                    :items="field.items"
                    :label="field.text"
                    item-text="text"
                    item-value="key"
                    clearable
                    @clear="
                      newTax = {}
                      onNewTaxInput()
                    "
                  />
                  <v-text-field v-if="newTax.key" v-model="newTax.percent" label="Percent" @input="onNewTaxInput" />
                  <v-text-field v-if="newTax.key" v-model="newTax.value" label="Valor" @input="onNewTaxInput" />
                </div>
                <v-text-field v-else v-model="field.value" :label="field.text" />
              </v-card>
            </v-card>
          </v-card-text>

          <v-card-actions>
            <v-btn color="warning" @click="resetFormField">Cancelar</v-btn>
            <v-btn
              color="success"
              @click="
                rewriteValuesFormDialog = false
                getDetails()
              "
            >
              OK
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-btn color="warning" :disabled="downloading" :loading="loading" rounded x-large @click="send(false)">
        <v-icon>mdi-email-send</v-icon>
      </v-btn>
      <v-btn
        target="_blank"
        :href="downloadURL"
        color="info"
        :loading="downloading"
        :disabled="loading"
        rounded
        x-large
        @click="downloadURL ? (downloadURL = null) : send(true)"
      >
        <span v-if="downloadURL">PDF</span>
        <v-icon v-else>mdi-download</v-icon>
      </v-btn>
    </v-card-actions>

    <v-card-text v-if="sendingEmail">
      <v-progress-linear v-if="loading" indeterminate />
      <v-alert v-else color="success">Enviado</v-alert>
    </v-card-text>

    <v-card-text v-else style="max-width: 600px">
      <!-- eslint-disable-next-line vue/no-v-html -->
      <v-sheet light v-html="htmlDetails" />
    </v-card-text>

    <v-btn
      v-if="!loading"
      rounded
      outlined
      block
      color="info"
      @click="sendingEmail ? (sendingEmail = false) : $emit('return')"
    >
      Atrás
      <v-icon>mdi-keyboard-return</v-icon>
    </v-btn>
  </v-card>
</template>

<script>
const defaultFields = [
  {
    text: 'Nombre del cliente',
    value: null,
    name: 'client_name',
  },
  {
    text: 'Email del cliente',
    value: null,
    name: 'client_email',
  },
  {
    text: 'Teléfono del cliente',
    value: null,
    name: 'client_phone',
  },
  {
    text: 'CUPS',
    value: null,
    name: 'cups',
  },
  {
    text: 'Importe alquiler equipo',
    value: null,
    name: 'rental',
  },

  // {
  //   id: 5004,
  //   company_name: 'AXPO',
  //   company_logo: '/media/6.png',
  //   name: 'AXPO-LUZ-ANTIGUO',
  //   tarif: '2.0TD',
  //   p1: 0.0,
  //   p2: 0.0,
  //   p3: 0.0,
  //   p4: 0.0,
  //   p5: 0.0,
  //   p6: 0.0,
  //   c1: 0.0,
  //   c2: 0.0,
  //   c3: 0.0,
  //   c4: 0.0,
  //   c5: 0.0,
  //   c6: 0.0,
  //   is_price_permanent: 'Fijo',
  //   client_type: 1,
  //   description: 'AXPO-ANTIGUO',
  //   c_st_p1: '21,12 kW/h × 10 dias × 0,0 € = 0,0 €',
  //   c_st_p2: None,
  //   c_st_p3: None,
  //   c_st_p4: None,
  //   c_st_p5: None,
  //   c_st_p6: None,
  //   c_st_c1: '22,12 kW/h × 0,0 € = 0,0 €',
  //   c_st_c2: None,
  //   c_st_c3: None,
  //   c_st_c4: None,
  //   c_st_c5: None,
  //   c_st_c6: None,
  //   st_p1: 0.0,
  //   st_p2: 0.0,
  //   st_p3: 0.0,
  //   st_p4: 0.0,
  //   st_p5: 0.0,
  //   st_p6: 0.0,
  //   st_c1: 0.0,
  //   st_c2: 0.0,
  //   st_c3: 0.0,
  //   st_c4: 0.0,
  //   st_c5: 0.0,
  //   st_c6: 0.0,
  //   tax: { percent: 5.11, value: '0.00' },
  //   iva: { percent: '21%', value: '0.06' },
  //   rental: 0.27,
  //   total: '0.32',
  //   current_price: 50.0,
  //   profit: '49.68',
  //   profit_num: '49.68',
  //   profit_percent: 99,
  //   annual_profit: '1813.2',
  //   annual_profit_num: '1813.20',
  //   kind: 'luz',
  //   reactive: 0.0,
  // },

  {
    text: 'Impuesto con desplegable',
    items: [
      { key: 'tax', value: '0.00', text: 'IGIC' },
      { key: 'iva', value: '0.06', text: 'IVA' },
      { key: 'canarias', value: null, text: 'islas Canarias' },
    ],
    name: 'impuesto',
  },
  {
    text: 'Nombre del asesor/a',
    value: null,
    name: 'agent',
  },
  {
    text: 'Teléfono del asesor/a',
    value: null,
    name: 'agent_phone',
  },
  {
    text: 'Email del asesor/a',
    value: null,
    name: 'agent_email',
  },
  {
    text: 'P1 (potencia)',
    value: null,
    name: 'up1',
  },
  {
    text: 'P2 (potencia)',
    value: null,
    name: 'up2',
  },
  {
    text: 'P3 (potencia)',
    value: null,
    name: 'up3',
  },
  {
    text: 'P4 (potencia)',
    value: null,
    name: 'up4',
  },
  {
    text: 'P5 (potencia)',
    value: null,
    name: 'up5',
  },
  {
    text: 'P6 (potencia)',
    value: null,
    name: 'up6',
  },
  {
    text: 'P1 (consumo)',
    value: null,
    name: 'uc1',
  },
  {
    text: 'P2 (consumo)',
    value: null,
    name: 'uc2',
  },
  {
    text: 'P3 (consumo)',
    value: null,
    name: 'uc3',
  },
  {
    text: 'P4 (consumo)',
    value: null,
    name: 'uc4',
  },
  {
    text: 'P5 (consumo)',
    value: null,
    name: 'uc5',
  },
  {
    text: 'P6 (consumo)',
    value: null,
    name: 'uc6',
  },
]
export default {
  name: 'CalculatorDetails',
  props: {
    offer: {
      type: Object,
      default: () => null,
    },
  },
  data() {
    return {
      newTax: {},
      form: null,
      rewriteValuesFormDialog: false,
      rewriteValuesForm: defaultFields,
      sendingEmail: false,
      loading: false,
      downloading: false,
      htmlDetails: null,
      otros: null,
      descuento: null,
      error: null,
      downloadURL: null,
    }
  },
  computed: {
    isGas() {
      return this.offer.kind === 'gas'
    },
  },
  async mounted() {
    this.form = {
      id: this.offer.id,
      ...this.$store.state.calculatorForm,
      with_calculations: true,
    }
    await this.getDetails()
  },
  methods: {
    // showInput(letter, number) {
    //   return this.form.tarif ? constants.showInput(letter, number, this.form.tarif) : false
    // },
    onNewTaxInput() {
      if (this.newTax.value) {
        this.rewriteValuesForm.push({
          name: this.newTax.key,
          value: { percent: this.newTax.percent, value: this.newTax.value },
        })
      } else {
        this.rewriteValuesForm = this.rewriteValuesForm.filter((item) => item.name !== this.newTax.key)
      }
    },
    resetFormField() {
      this.rewriteValuesForm = defaultFields
      this.rewriteValuesFormDialog = false
    },
    async getDetails() {
      this.loading = true
      const form = Object.fromEntries(
        Object.entries(this.form)
          .filter((i) => [undefined, null, ''].indexOf(i[1]) === -1)
          .map((item) => {
            const [key, val] = item
            if (typeof val === 'string' && val.includes(',')) {
              return [key, val.replaceAll(',', '.')]
            }
            return [key, val]
          }),
      )
      try {
        this.htmlDetails = await this.$axios.$post('calculator/new_offer/', {
          ...form,
          rewrite: Object.fromEntries(
            this.rewriteValuesForm.map((item) => {
              const { name, value } = item
              return [name, value]
            }),
          ),
        })
      } catch (e) {
        let err = e.response.data
        err = err instanceof Array ? err.join('; ') : err
        await this.$swal({ title: 'Error', icon: 'error', text: err })
      } finally {
        this.loading = false
      }
    },
    async send(download) {
      if (!download && !this.rewriteValuesForm['EMAIL DEL CLIENTE']) {
        await this.$swal({ title: 'Entrar correo', icon: 'error' })
        return
      }
      this.sendingEmail = !download
      await this.$vuetify.goTo(0)
      if (download) {
        this.downloading = true
      } else {
        this.loading = true
      }
      const data = { ...this.form, rewrite: { ...this.rewriteValuesForm } }
      if (download) {
        data.download = 'true'
      } else {
        data.send = 'true'
      }
      try {
        const response = await this.$axios.$post('calculator/new_offer/', { ...data })
        if (download) this.downloadURL = `${location.origin}/${response}`
      } catch (e) {
        await this.$swal({
          title: 'Error',
          icon: 'error',
          text: JSON.parse(e && e.response && e.response.data ? e.response.data : e),
        })
      } finally {
        this.loading = this.downloading = false
      }
    },
  },
}
</script>
