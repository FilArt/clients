<template>
  <v-card>
    <v-card-title>Oferta</v-card-title>
    <v-card-text>
      <detail-offer :offer="bid.offer" />
    </v-card-text>

  <v-divider />

    <v-card-title>Client data</v-card-title>
    <v-card-text>
      <p>DNI: {{ bid.user.dni }}</p>
      <p>CIF/DNI: {{ bid.user.cif_dni }}</p>
      <p>Legal representative: {{ bid.user.legal_representative }}</p>
      <p>IBAN: {{ bid.user.iban }}</p>
      <p>EMAIL: {{ bid.user.email }}</p>
    </v-card-text>

    <v-divider />

    <v-card-title>Puntos</v-card-title>
    <v-card-text>
      <puntos-list :puntos="bid.puntos" />
    </v-card-text>

    <v-card-actions>
      <v-dialog v-model="submitDialog">
        <template v-slot:activator="{ on }">
          <v-btn color="primary" v-on="on" block>
            Enviar
            <v-icon right>mdi-check</v-icon>
          </v-btn>
        </template>
        <v-card>
          <v-card-title>
            <p class="flex-grow-1">Enviar</p>
            <close-button @click="submitDialog = false" />
          </v-card-title>
          <v-card-text>
            <v-form @submit.prevent="submit" novalidate>
              <status-select
                v-model="data.status"
                :errors="errorMessages.status"
              />
              <v-textarea
                v-model="data.message"
                label="Message"
                :placeholder="
                  data.status === 'success'
                    ? 'Contrato celebrado!'
                    : 'No puede hacer un contrato porque...'
                "
              />

              <v-card-actions>
                <v-btn
                  block
                  type="submit"
                  color="success"
                  :disabled="!data.status || !data.message"
                >
                  Listo
                  <v-icon right>mdi-check</v-icon>
                </v-btn>
              </v-card-actions>
            </v-form>
          </v-card-text>
        </v-card>
      </v-dialog>
    </v-card-actions>
  </v-card>
</template>

<script>
import DetailOffer from '~/components/detailOffer'
import StatusSelect from '~/components/selects/StatusSelect'
import CloseButton from '~/components/buttons/closeButton'
import SubmitButton from '~/components/buttons/submitButton'
export default {
  components: {
    SubmitButton,
    CloseButton,
    StatusSelect,
    DetailOffer,
    PuntosList: () => import('~/components/puntos/PuntosList'),
  },
  async asyncData({ $axios, params, store }) {
    const bid = await $axios.$get(`bids/bids/${params.id}`)
    let puntoHeaders = store.state.puntoHeaders
    if (!puntoHeaders || !puntoHeaders.length) {
      puntoHeaders = await $axios.$get('/users/puntos/get_headers/')
      store.commit('setPuntoHeaders', puntoHeaders)
    }
    return {
      bid,
      puntoHeaders,
    }
  },
  data() {
    return {
      submitDialog: false,
      data: {
        status: null,
        message: null,
      },
      errorMessages: { status: null, message: null },
    }
  },
  methods: {
    submit() {
      this.$axios
        .$post(`bids/bids/${this.bid.id}/validate/`, this.data)
        .then((data) => {
          this.bid = data
          this.$swal({
            title: 'Listo',
            icon: 'success',
          }).then(() => this.$router.push('/support'))
        })
        .catch((e) => (this.errorMessages = e.response.data))
    },
  },
}
</script>
