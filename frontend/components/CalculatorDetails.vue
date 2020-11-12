<template>
  <v-card elevation="0">
    <v-card-text>
      <v-text-field v-model="clientName" label="Nombre" />
      <email-field v-model="emailTo" />
      <v-checkbox v-model="showAdditionalFields" label="Extra campos" />
    </v-card-text>

    <v-card-text v-show="showAdditionalFields">
      <v-card-title>Extra campos</v-card-title>
      <v-text-field v-model="direccion" label="Direccion" type="number" />
      <v-text-field v-model="cups" label="CUPS" type="number" />
      <v-text-field v-model="p1_offer" label="Precio por potencia P1 facturacion actual" type="number" />
      <v-text-field
        v-show="showInput('p', 2)"
        v-model="p2_offer"
        label="Precio por potencia P2 facturacion actual"
        type="number"
      />
      <v-text-field
        v-show="showInput('p', 3)"
        v-model="p3_offer"
        label="Precio por potencia P3 facturacion actual"
        type="number"
      />
      <v-text-field v-model="c1_offer" label="Precio por consumo P1 facturacion actual" type="number" />
      <v-text-field
        v-show="showInput('c', 2)"
        v-model="c2_offer"
        label="Precio por consumo P2 facturacion actual"
        type="number"
      />
      <v-text-field
        v-show="showInput('c', 3)"
        v-model="c3_offer"
        label="Precio por consumo P3 facturacion actual"
        type="number"
      />
    </v-card-text>

    <v-card-text v-html="htmlDetails" />

    <v-btn color="warning" :loading="loading" fixed right bottom rounded x-large @click="send">
      <v-icon>mdi-email-send</v-icon>
    </v-btn>
    <v-btn style="margin-right: 7em" color="success" :loading="loading" fixed right bottom rounded @click="getDetails">
      <v-icon>mdi-refresh</v-icon>
    </v-btn>
  </v-card>
</template>

<script>
import { mapState } from 'vuex'
import EmailField from '@/components/fields/emailField'
import constants from '@/lib/constants'

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
      loading: false,
      calculations: [],
      htmlDetails: null,
      direccion: null,
      cups: null,
      clientName: null,
      emailTo: null,
      showAdditionalFields: false,
      p1_offer: null,
      p2_offer: null,
      p3_offer: null,
      c1_offer: null,
      c2_offer: null,
      c3_offer: null,
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
    showInput(letter, number) {
      return constants.showInput(letter, number, this.form.tarif)
    },
    async getDetails() {
      if (!this.offer || !this.form || !this.tarif) return
      this.loading = true
      const { data, params } = this.getDataAndParams()
      this.htmlDetails = await this.$axios.$get(`calculator/new_offer/?${params}`)
      this.calculations = await this.$axios.$post('calculator/calculate/', data)
      this.$emit('calculations', this.calculations)
      this.loading = false
    },
    async send() {
      if (!this.emailTo) {
        await this.$swal({ title: 'Entrar correo', icon: 'error' })
        return
      }
      this.loading = true
      const { params } = this.getDataAndParams()
      try {
        await this.$axios.$get(`calculator/new_offer/?send=true&${params}`)
        await this.$swal({ title: 'Sent...', icon: 'success' })
      } catch (e) {
        await this.$swal({ title: 'Not sent!', icon: 'error', text: e.response.data })
      } finally {
        this.loading = false
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
        p1_offer: this.p1_offer,
        p2_offer: this.p2_offer,
        p3_offer: this.p3_offer,
        c1_offer: this.c1_offer,
        c2_offer: this.c2_offer,
        c3_offer: this.c3_offer,
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
