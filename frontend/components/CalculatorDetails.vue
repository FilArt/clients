<template>
  <v-card elevation="0">
    <v-card-text>
      <v-row class="text-center">
        <v-col>
          <v-btn rounded color="success" icon @click="getHtmlDetails">
            <v-icon>mdi-refresh</v-icon>
          </v-btn>
        </v-col>

        <v-col>
          <v-btn class="pa-0" color="warning" :disabled="downloading" :loading="loading" rounded @click="send(false)">
            <v-icon>mdi-email-send</v-icon>
          </v-btn>
        </v-col>

        <v-col>
          <v-btn
            target="_blank"
            :href="downloadURL"
            color="info"
            :loading="downloading"
            :disabled="loading"
            rounded
            @click="downloadURL ? (downloadURL = null) : send(true)"
          >
            <span v-if="downloadURL">PDF</span>
            <v-icon v-else>mdi-download</v-icon>
          </v-btn>
        </v-col>

        <v-col>
          <propuesta v-model="calculatedValues" @update="onUpdateForm($event)" />
        </v-col>
      </v-row>
    </v-card-text>

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
import qs from 'qs'

export default {
  name: 'CalculatorDetails',
  components: { Propuesta: () => import('@/components/Propuesta') },
  props: {
    offer: {
      type: Object,
      default: () => null,
    },
  },
  data() {
    return {
      form: null,
      rewriteValuesForm: {},
      calculatedValues: {},
      rewriteValuesFormDialog: false,
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
  async created() {
    this.form = {
      id: this.offer.id,
      ...this.$store.state.calculatorForm,
    }
    await this.getHtmlDetails()
  },
  methods: {
    async onUpdateForm({ key, value }) {
      this.rewriteValuesForm[key] = value
      this.calculatedValues[key] = value
      await this.getHtmlDetails()
    },
    getForm() {
      const data = {
        ...this.form,
        ...this.rewriteValuesForm,
        ...qs.parse(location.search),
      }
      return Object.fromEntries(
        Object.entries(data)
          .filter((i) => [undefined, null, ''].indexOf(i[1]) === -1)
          .map((item) => {
            const [key, val] = item
            if (typeof val === 'string' && val.includes(',')) {
              return [key, val.replaceAll(',', '.')]
            }
            return [key, val]
          }),
      )
    },
    async getHtmlDetails() {
      this.loading = true
      const form = this.getForm()
      try {
        this.calculatedValues = await this.$axios.$post('calculator/new_offer/', { ...form, just_get: true })
        this.htmlDetails = await this.$axios.$post('calculator/new_offer/', form)
      } catch (e) {
        let err = e.response.data
        err = err instanceof Array ? err.join('; ') : err
        await this.$swal({ title: 'Error', icon: 'error', text: JSON.stringify(err) })
      } finally {
        this.loading = false
      }
    },
    async send(download) {
      if (!download && !this.rewriteValuesForm['client_email']) {
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
      const data = this.getForm()
      if (download) {
        data.download = 'true'
      } else {
        data.send = 'true'
      }
      try {
        const response = await this.$axios.$post('calculator/new_offer/', data)
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
