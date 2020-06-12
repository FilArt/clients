<template>
  <v-container>
    <v-fab-transition>
      <v-btn
        v-if="!isBottomIntersecting && !isTopIntersecting"
        min-width="30%"
        color="primary"
        fixed
        style="z-index: 1000;"
        bottom
        rounded
        right
        nuxt
        :to="back"
      >
        Back
        <v-icon right>mdi-keyboard-return</v-icon>
      </v-btn>
    </v-fab-transition>

    <div>
      <v-card
        v-intersect="onIntersectTop"
        elevation="0"
        style="margin-bottom: 1em;"
      >
        <return-button v-if="!isBottomIntersecting" :to="back" />
      </v-card>

      <v-card
        v-for="offer in offers"
        :key="offer.id"
        style="margin-bottom: 1em;"
      >
        <v-row justify="space-between">
          <v-col cols="auto">
            <v-img
              :src="offer.company_logo || '/no-image.svg'"
              max-width="600"
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
                      desde {{ offer.power_min }} kW hasta
                      {{ offer.power_max }} kW
                    </td>
                  </tr>

                  <tr>
                    <td>Consumo anual:</td>
                    <td>
                      desde {{ offer.consumption_min }} kW/h hasta
                      {{ offer.consumption_max }}
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
            <v-card-actions>
              <v-btn
                rounded
                block
                outlined
                color="success"
                @click="addBid(offer.id)"
              >
                Add to portfel<v-icon right>mdi-briefcase</v-icon>
              </v-btn>
            </v-card-actions>
          </v-col>
        </v-row>
      </v-card>
      <v-card v-intersect="onIntersectBottom" elevation="0">
        <return-button :to="back" />
      </v-card>
    </div>
  </v-container>
</template>

<script>
export default {
  components: {
    ReturnButton: () => import('~/components/buttons/returnButton'),
    RefreshButton: () => import('~/components/buttons/refreshButton'),
    CancelButton: () => import('~/components/buttons/cancelButton'),
  },
  data() {
    return {
      isBottomIntersecting: false,
      isTopIntersecting: true,
    }
  },
  async asyncData({ $axios, params, query }) {
    const offers = await $axios.$get(
      `calculator/offers/?by_name_id=${params.id}`
    )
    return {
      offers,
      back: query.back ? query.back.replace(/@/, '&') : '/offers',
    }
  },
  methods: {
    onIntersectBottom(entries) {
      this.isBottomIntersecting = entries[0].isIntersecting
    },
    onIntersectTop(entries) {
      this.isTopIntersecting = entries[0].isIntersecting
    },
    addBid(bidId) {
      let data = { offer: bidId }
      if (this.$route.query.fromCalculator === 'true') {
        data = this.$store.state.calculatorForm
        data.offer = bidId
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
