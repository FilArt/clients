<template>
  <v-card>
    <v-card-title>
      <p class="flex-grow-1">Contratar oferta {{ bid.id }}</p>
    </v-card-title>

    <v-card-text>
      <v-row>
        <v-col> Puntos suministros ({{ puntos.length }}) </v-col>
      </v-row>
      <v-row align="center" class="text-center">
        <v-col v-for="(punto, idx) in puntos" :key="idx">
          <punto-detail-dialog
            closeable
            color="green"
            :offer-client-type="bid.offer.client_type"
            :bid-id="bid.id"
            :punto="punto"
            :label="`Punto suministro #${idx + 1}`"
            @fetch-puntos="fetchPuntos"
          />
        </v-col>
      </v-row>
    </v-card-text>

    <v-card-text>
      <v-row>
        <v-col>
          <add-punto
            color="primary"
            :offer-client-type="bid.offer.client_type"
            :bid-id="bid.id"
            label="Añadir nuevo punto suministro"
            @fetch-puntos="contractar"
          />
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  components: {
    PuntoDetailDialog: () => import('@/components/puntos/PuntoDetailDialog'),
    AddPunto: () => import('~/components/puntos/AddPunto'),
  },
  async asyncData({ $axios, params }) {
    const bid = await $axios.$get(`bids/bids/${params.id}/`)
    const puntos = await $axios.$get(`/users/puntos/?bid=${bid.id}`)
    return {
      puntos,
      bid,
    }
  },
  methods: {
    async fetchPuntos() {
      this.puntos = []
      this.puntos = await this.$axios.$get(`/users/puntos/?bid=${this.bid.id}`)
    },
    async contractar() {
      await this.$router.push(`/bids/${this.bid.id}`)
      await this.$swal({
        title: 'Contratado!',
        icon: 'success',
      })
    },
  },
}
</script>
