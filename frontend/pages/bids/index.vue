<template>
  <v-card>
    <v-alert v-if="bids.length === 0">
      Nohay solicitud.
    </v-alert>

    <div v-else>
      <v-card-title>
        <p class="flex-grow-1">Cartera</p>
        <status-select v-model="status" />
      </v-card-title>

      <v-card-text>
        <v-list nav shaped subheader>
          <v-list-item>
            <v-col>
              <small>
                №
              </small>
            </v-col>

            <v-list-item>
              Oferta
            </v-list-item>
            <v-list-item>Fecha de creacion</v-list-item>
            <v-list-item>Estado</v-list-item>
          </v-list-item>

          <v-list-item
            v-for="bid in (status ? bids.filter(b => status ? b.status === status.text : true) : bids)"
            :key="bid.id"
            :to="`/bids/${bid.id}`"
            nuxt
          >
            <v-col>
              <small>{{ bid.id }}</small>
            </v-col>

            <v-list-item-title>
              {{ bid.offer_name }}
            </v-list-item-title>

            <v-list-item-title>
              {{ bid.created_at }}
            </v-list-item-title>

            <v-list-item-title>
              {{ bid.status }}
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-card-text>

      <go-up-button />
    </div>
  </v-card>
</template>

<script>
export default {
  components: {
    GoUpButton: () => import('~/components/buttons/goUpButton'),
    StatusSelect: () => import('~/components/selects/StatusSelect'),
    ClientTypeSelect: () => import('~/components/selects/ClientTypeSelect'),
  },
  data() {
    return {
      status: null,
    }
  },
  async asyncData({ $axios }) {
    const bids = await $axios.$get('bids/')
    return { bids }
  },
}
</script>
