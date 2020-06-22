<template>
  <v-row justify="space-between" align="center">
    <v-col>
      <v-img
        class="mx-auto"
        :src="offer.company_logo || '/no-image.svg'"
        max-width="400"
      />
    </v-col>

    <v-col>
      <v-card-title>
        {{ offer.name }}
      </v-card-title>
      <v-divider />
      <v-card-text>
        <v-simple-table class="pa-0" style="max-width: 100%;">
          <template v-slot:default>
            <tr>
              <td>Comercializadora</td>
              <td>{{ offer.company }}</td>
            </tr>
            <tr>
              <td colspan="2">{{ offer.description }}</td>
            </tr>

            <tr>
              <td>Tarif:</td>
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
              <td>Typo de oferta:</td>
              <td>
                {{ offer.client_type === 0 ? 'Particular' : 'Negocio' }}
              </td>
            </tr>

            <tr>
              <td>Precio por potencia:</td>
              <td class="d-flex">
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
              <td class="d-flex">
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
        <v-btn rounded block outlined color="success" @click="addBid(offer.id)">
          Add to portfel<v-icon right>mdi-briefcase</v-icon>
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
    addBid(bidId) {
      let data = { offer: bidId }
      if (this.$route.query.fromCalculator === 'true') {
        data = { ...data, ...this.$store.state.calculatorForm }
      }
      this.$axios.$post('bids/', data).then((createdBidData) => {
        this.$swal({
          title: 'Se ha agregado una solicitud de contrato a la cartera.',
          icon: 'success',
          buttons: {
            cancel: true,
            goToPortfel: {
              text: 'Go to portfel',
              value: 'bids',
            },
            goToBid: {
              text: 'Go to bid',
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
