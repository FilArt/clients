<template>
  <v-card elevation="0">
    <v-card-actions>
      <v-spacer />

      <v-btn style="margin-right: 7em" color="success" :disabled="loading || downloading" rounded @click="getDetails">
        <v-icon>mdi-refresh</v-icon>
      </v-btn>

      <v-dialog v-model="rewriteValuesFormDialog" max-width="max-content" scrollable>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on">Cambiar valores</v-btn>
        </template>
        <v-card>
          <v-card-title>Cambiar valores</v-card-title>

          <v-card-text>
            <v-card flat class="d-flex flex-wrap">
              <v-card v-for="field in rewriteValuesForm" :key="field.name" class="mb-4 pa-2" flat>
                <div
                  v-if="field.items && field.items.length"
                  :style="newTax.key ? 'border: 1px solid green; padding: 20px;' : null"
                >
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
                <decimal-field
                  v-else-if="field.name.length === 2 && (field.name.startsWith('p') || field.name.startsWith('c'))"
                  v-model="field.value"
                  :label="field.text"
                />
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
import decimalField from './fields/decimalField.vue'
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
  {
    text: 'Impuesto electricidad (%)',
    value: null,
    name: 'tax_percent',
  },
  {
    text: 'IVA (%)',
    value: null,
    name: 'iva_percent',
  },
  {
    text: 'IGIC (%)',
    value: null,
    name: 'igic_percent',
  },
  {
    text: 'P1 (precio de potencia)',
    value: null,
    name: 'p1',
  },
  {
    text: 'P2 (precio de potencia)',
    value: null,
    name: 'p2',
  },
  {
    text: 'P3 (precio de potencia)',
    value: null,
    name: 'p3',
  },
  {
    text: 'P4 (precio de potencia)',
    value: null,
    name: 'p4',
  },
  {
    text: 'P5 (precio de potencia)',
    value: null,
    name: 'p5',
  },
  {
    text: 'P6 (precio de potencia)',
    value: null,
    name: 'p6',
  },
  {
    text: 'P1 (precio de consumo)',
    value: null,
    name: 'c1',
  },
  {
    text: 'P2 (precio de consumo)',
    value: null,
    name: 'c2',
  },
  {
    text: 'P3 (precio de consumo)',
    value: null,
    name: 'c3',
  },
  {
    text: 'P4 (precio de consumo)',
    value: null,
    name: 'c4',
  },
  {
    text: 'P5 (precio de consumo)',
    value: null,
    name: 'c5',
  },
  {
    text: 'P6 (precio de consumo)',
    value: null,
    name: 'c6',
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
]
export default {
  name: 'CalculatorDetails',
  components: { decimalField },
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
        Object.entries({
          ...this.form,
          ...Object.fromEntries(
            this.rewriteValuesForm.map((item) => {
              const { name, value } = item
              return [name, value]
            }),
          ),
        })
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
        this.htmlDetails = await this.$axios.$post('calculator/new_offer/', form)
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
