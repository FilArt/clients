<template>
  <v-row justify="space-between" align="center">
    <v-col class="flex-grow-0">
      <v-img :src="offer.company_logo || '/no-image.svg'" max-width="400" />
    </v-col>

    <v-col>
      <v-card-title>{{ offer.name }}</v-card-title>
      <v-divider />
      <v-card-text>
        <v-simple-table class="offer-detail-table">
          <template v-slot:default>
            <tr>
              <td>ID:</td>
              <td>{{ offer.id }}</td>
            </tr>

            <tr>
              <td>Comercializadora:</td>
              <td>{{ offer.company }}</td>
            </tr>

            <br />

            <tr>
              <td colspan="2">{{ offer.description }}</td>
            </tr>

            <br />

            <tr>
              <td>Tarifa:</td>
              <td>{{ offer.tarif }}</td>
            </tr>

            <tr>
              <td>Potencia contratada:</td>
              <td>
                desde {{ offer.power_min }} kW hasta {{ offer.power_max }} kW
              </td>
            </tr>

            <tr>
              <td>Consumo anual:</td>
              <td>
                desde {{ offer.consumption_min }} kW/h hasta
                {{ offer.consumption_max.toString().substr(0, 5) }}
                kW/h
              </td>
            </tr>

            <tr>
              <td>Tipo de oferta:</td>
              <td>{{ offer.client_type === 0 ? 'Físico' : 'Juridico' }}</td>
            </tr>

            <tr>
              <td>Precio por potencia:</td>
              <td>
                <v-chip
                  v-for="p in ['p1', 'p2', 'p3'].filter((p) => offer[p])"
                  :key="p"
                >
                  {{ p.toUpperCase() }}:
                  {{ offer[p] ? offer[p] + ' €' : '-' }}
                </v-chip>
              </td>
            </tr>

            <tr>
              <td>Precio por consumo:</td>
              <td>
                <v-chip
                  v-for="p in ['c1', 'c2', 'c3'].filter((p) => offer[p])"
                  :key="p"
                >
                  {{ p.replace('c', 'p').toUpperCase() }}:
                  {{ offer[p] ? offer[p] + ' €' : '-' }}
                </v-chip>
              </td>
            </tr>
          </template>
        </v-simple-table>
      </v-card-text>
      <v-card-actions v-if="showActions">
        <v-btn rounded block outlined color="primary" @click="addBid">
          Añadir a cartera
          <v-icon right>mdi-briefcase</v-icon>
        </v-btn>
      </v-card-actions>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'detailOffer',
  props: {
    showActions: {
      type: Boolean,
      default: false,
    },
    offer: {
      type: Object,
      default: () => null,
    },
  },
  methods: {
    addBid() {
      if (!this.offer) return
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

<style lang="sass" scoped>
.offer-detail-table
  th, td
    padding: 5px
    border-bottom: 1px solid #ddd
</style>
