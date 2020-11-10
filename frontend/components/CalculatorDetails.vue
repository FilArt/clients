<template>
  <v-card>
    <v-row>
      <v-col>
        <v-text-field v-model="direccion" label="Direccion" />
        <v-text-field v-model="cups" label="CUPS" />
        <v-text-field v-model="clientName" label="Nombre" />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-container fluid v-html="htmlDetails" />
      </v-col>
    </v-row>
  </v-card>
</template>

<script>
import { mapState } from 'vuex'

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
      calculations: [],
      htmlDetails: null,
      direccion: null,
      cups: null,
      clientName: null,
      interval: null,
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
    this.interval = setInterval(this.getDetails, 2000)
  },
  beforeDestroy() {
    clearInterval(this.interval)
  },
  methods: {
    async getDetails() {
      if (!this.offer || !this.form || !this.tarif) return
      const data = {
        ...this.form,
        id: this.offer.id,
        tarif: this.tarif,
        with_calculations: true,
        direccion: this.direccion,
        cups: this.cups,
        client_name: this.clientName,
      }
      const params = Object.keys(data)
        .filter((key) => data[key] !== null)
        .map((key) => `${key}=${data[key]}`)
        .join('&')
      this.htmlDetails = await this.$axios.$get(`calculator/new_offer/?${params}`)
      this.calculations = await this.$axios.$post('calculator/calculate/', data)
      this.$emit('calculations', this.calculations)
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
