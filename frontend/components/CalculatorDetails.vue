<template>
  <v-card elevation="0">
    <v-card-actions>
      <v-spacer />
      <v-btn style="margin-right: 7em" color="success" :disabled="loading" rounded @click="getDetails">
        <v-icon>mdi-refresh</v-icon>
      </v-btn>
      <v-btn color="warning" :loading="loading" rounded x-large @click="send">
        <v-icon>mdi-email-send</v-icon>
      </v-btn>
    </v-card-actions>

    <v-card-text v-if="sendingEmail">
      <v-progress-linear v-if="loading" indeterminate />
      <v-alert v-else color="success">Enviado</v-alert>
      <v-btn v-if="!loading" rounded outlined block color="#004680" @click="sendingEmail = false">
        Atrás
        <v-icon>mdi-keyboard-return</v-icon>
      </v-btn>
    </v-card-text>

    <div v-else>
      <v-card-text>
        <v-row>
          <v-col>
            <template>
              <v-text-field v-model="agent.fullname" label="Tu nombre" />
              <email-field v-model="agent.email" label="Tu email" />
              <phone-field v-model="agent.phone" />
            </template>

            <v-text-field v-model="clientName" label="Nombre de cliente" />
            <email-field v-model="emailTo" label="Email de cliente" />
          </v-col>
          <v-col>
            <v-text-field v-model="offerName" dense label="Oferta" />
            <v-text-field v-model="direccion" dense label="Direccion" />
            <v-text-field v-model="cups" dense label="CUPS" />
            <v-text-field v-model="p1_offer" dense :label="`Precio por ${word} ${isGas ? '' : 'P1'}`" type="number" />
            <v-text-field
              v-show="showInput('p', 2)"
              v-model="p2_offer"
              dense
              :label="`Precio por ${word} ${isGas ? '' : 'P2'}`"
              type="number"
            />
            <v-text-field
              v-show="showInput('p', 3)"
              v-model="p3_offer"
              dense
              :label="`Precio por ${word} ${isGas ? '' : 'P3'}`"
              type="number"
            />
            <v-text-field v-model="c1_offer" :label="`Precio por consumo ${isGas ? '' : 'P1'}`" type="number" dense />
            <v-text-field
              v-show="showInput('c', 2)"
              v-model="c2_offer"
              dense
              :label="`Precio por consumo ${isGas ? '' : 'P2'}`"
              type="number"
            />
            <v-text-field
              v-show="showInput('c', 3)"
              v-model="c3_offer"
              dense
              :label="`Precio por consumo ${isGas ? '' : 'P3'}`"
              type="number"
            />
            <v-text-field v-model="otros" label="Otros" type="number" />
            <v-text-field v-model="descuento" label="Descuento" suffix="€" type="number" />

            <v-text-field v-model="rental" label="Alquiler de equipo" type="number" dense />
            <v-text-field v-model="tax" label="Imp.Electricidad" type="number" dense />
            <v-text-field v-model="iva" :label="form.igic ? 'IGIC' : 'IVA'" suffix="%" type="number" dense />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-textarea v-model="note" label="Nota" dense />
          </v-col>
        </v-row>
      </v-card-text>

      <v-card-text>
        <v-sheet light v-html="htmlDetails" />
      </v-card-text>
    </div>
  </v-card>
</template>

<script>
import { mapState } from 'vuex'
import EmailField from '@/components/fields/emailField'
import constants from '@/lib/constants'
import PhoneField from '@/components/fields/phoneField'

export default {
  name: 'CalculatorDetails',
  components: { PhoneField, EmailField },
  props: {
    offer: {
      type: Object,
      default: () => null,
    },
  },
  data() {
    const user = this.$auth.user || {}
    let agent = localStorage.getItem('agent')
    agent =
      agent && typeof agent === 'string'
        ? JSON.parse(agent)
        : { fullname: user.fullname, email: user.email, phone: user.phone }
    return {
      sendingEmail: false,
      loading: false,
      htmlDetails: null,
      direccion: null,
      cups: null,
      clientName: null,
      emailTo: null,
      p1_offer: null,
      p2_offer: null,
      p3_offer: null,
      c1_offer: null,
      c2_offer: null,
      c3_offer: null,
      offerName: null,
      note: null,
      rental: null,
      tax: null,
      iva: 21,
      otros: null,
      descuento: null,
      agent,
      error: null,
    }
  },
  computed: {
    ...mapState({
      form: (state) => state.calculatorForm,
    }),
    isGas() {
      return this.offer.kind === 'gas'
    },
    word() {
      return this.isGas ? 'termino fijo' : 'potencia'
    },
  },
  watch: {
    agent: {
      handler: (val) => {
        localStorage.setItem('agent', JSON.stringify(val))
      },
      deep: true,
    },
  },
  async mounted() {
    await this.getDetails()
  },
  methods: {
    showInput(letter, number) {
      return this.form.tarif ? constants.showInput(letter, number, this.form.tarif) : false
    },
    async getDetails() {
      this.loading = true
      const { params } = this.getDataAndParams()
      this.htmlDetails = await this.$axios.$get(`calculator/new_offer/?${params}`)
      this.loading = false
    },
    async send() {
      if (!this.emailTo) {
        await this.$swal({ title: 'Entrar correo', icon: 'error' })
        return
      }
      this.sendingEmail = true
      this.$vuetify.goTo(0)
      this.loading = true
      const { params } = this.getDataAndParams()
      try {
        await this.$axios.$get(`calculator/new_offer/?send=true&${params}`)
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
        tarif: this.form.tarif,
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
        name: this.offerName,
        note: this.note,
        rental: this.rental,
        tax: this.tax,
        agent_email: this.agent.email,
        agent_fullname: this.agent.fullname,
        agent_phone: this.agent.phone,
        iva: this.iva,
        otros: this.otros,
        descuento: this.descuento,
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
