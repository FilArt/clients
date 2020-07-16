<template>
  <v-card>
    <v-card-text class="text-center">
      <div class="text-h4">
        La sección de cartera en nuestro sitio web es un análogo de la cesta
      </div>

      <div class="text-h6">
        En esta sección puede guardar las ofertas que le interesan, así como
        controlar el estado de su perfil
      </div>
    </v-card-text>

    <v-alert v-if="bids.length === 0">Nohay solicitud.</v-alert>

    <div v-else>
      <v-card-text>
        <v-list nav shaped subheader>
          <v-list-item>
            <v-col>№</v-col>
            <v-list-item>Oferta</v-list-item>
            <v-list-item>Fecha de creación</v-list-item>
            <v-list-item>Estado</v-list-item>
          </v-list-item>

          <v-list-item
            v-for="bid in bids"
            :key="bid.id"
            :to="`/bids/${bid.id}`"
            nuxt
          >
            <v-col>
              <small>{{ bid.id }}</small>
            </v-col>

            <v-list-item-title>{{ bid.offer_name }}</v-list-item-title>

            <v-list-item-title>{{ bid.created_at }}</v-list-item-title>

            <v-list-item-title>{{ bid.status }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-card-text>
    </div>
  </v-card>
</template>

<script>
export default {
  async asyncData({ $axios }) {
    const bids = await $axios.$get('bids/bids/')
    return { bids }
  },
}
</script>
