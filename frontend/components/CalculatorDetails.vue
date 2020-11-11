<template>
  <v-card>
    <v-row>
      <v-col>
        <v-text-field v-model="direccion" label="Direccion" />
        <v-text-field v-model="cups" label="CUPS" />
        <v-text-field v-model="clientName" label="Nombre" />
        <email-field v-model="emailTo" />
      </v-col>
    </v-row>

    <v-card-text v-html="htmlDetails" />

    <v-card-actions>
      <v-btn @click="getDetails">Refresh</v-btn>
      <v-btn @click="send">Send me</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapState } from 'vuex'
import EmailField from '@/components/fields/emailField'

export default {
  name: 'CalculatorDetails',
  components: { EmailField },
  props: {
    offer: {
      type: Object,
      default: () => null,
    },
  },
  data() {
    return {
      calculations: [],
      htmlDetails: null,
      direccion: null,
      cups: null,
      clientName: null,
      emailTo: null,
    }
  },
  computed: {
    ...mapState({
      form: (state) => state.calculatorForm,
      tarif: (state) => state.tarif,
    }),
    terminos() {
      return [
        { text: `Termino de ${this.offer.kind === 'luz' ? 'potencia' : 'fijo'}`, items: 'p' },
        { text: 'Termino de energia', items: 'c' },
      ].map((termino) => {
        return {
          ...termino,
          items: [1, 2, 3]
            .map((number) => ({
              text: `${termino.items.toUpperCase()}${number}`,
              value: this.calculations[`c_st_${termino.items}${number}`],
            }))
            .filter((t) => t.value),
        }
      })
    },
  },
  async mounted() {
    await this.getDetails()
  },
  methods: {
    async getDetails() {
      if (!this.offer || !this.form || !this.tarif) return
      const { data, params } = this.getDataAndParams()
      this.htmlDetails = await this.$axios.$get(`calculator/new_offer/?${params}`)
      this.calculations = await this.$axios.$post('calculator/calculate/', data)
      this.$emit('calculations', this.calculations)
    },
    async send() {
      const { params } = this.getDataAndParams()
      try {
        await this.$axios.$get(`calculator/new_offer/?send=true&${params}`)
        await this.$swal({ title: 'Sent...', icon: 'success' })
      } catch (e) {
        await this.$swal({ title: 'Not sent!', icon: 'error', text: e.response.data })
      }
    },
    getDataAndParams() {
      const data = {
        ...Object.fromEntries(Object.entries(this.form).filter((i) => [undefined, null, ''].indexOf(i[1]) === -1)),
        id: this.offer.id,
        tarif: this.tarif,
        with_calculations: true,
        direccion: this.direccion,
        cups: this.cups,
        client_name: this.clientName,
        email_to: this.emailTo,
      }
      const params = Object.keys(data)
        .filter((key) => data[key] !== null)
        .map((key) => `${key}=${data[key]}`)
        .join('&')
      return { data, params }
    },
    addBid() {
      let data = { offer: this.offer.id }
      if (this.$route.query.fromCalculator === 'true') {
        data = { ...data, ...this.$store.state.calculatorForm }
      }
      this.$axios.$post('bids/bids/', data).then((createdBidData) => {
        this.$swal({
          title: 'Se ha agregado una solicitud de contrato a la cartera.',
          icon: 'success',
          buttons: {
            cancel: true,
            goToPortfel: {
              text: 'Ir a Cartera',
              value: 'bids',
            },
            goToBid: {
              text: 'Contratar',
              value: 'bid',
            },
          },
        }).then((value) => {
          if (value === 'bids') {
            this.$router.push('/bids')
          } else if (value === 'bid') {
            this.$router.push(`/bids/${createdBidData.id}`)
          }
        })
      })
    },
  },
}
</script>

<style scoped>
.popusk {
  width: 2em;
}
.popusk-2 {
  flex-grow: 1;
}
@media only screen and (max-width: 768px) {
  /* For mobile phones: */
  .popusk {
    width: 0;
  }
  .popusk-2 {
    flex-grow: 3;
  }
}
</style>
