<template>
  <v-navigation-drawer permanent>
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title class="title">Solicitudes</v-list-item-title>
      </v-list-item-content>
    </v-list-item>

    <v-divider />

    <v-list dense nav>
      <v-list-item v-for="bid in bids" :key="bid.id" @click="$emit('chosen', bid.id)">
        <v-icon v-if="bid.offer_kind === 'luz'" color="warning">mdi-flash</v-icon>
        <v-icon v-else color="blue">mdi-fire</v-icon>
        <v-list-item-title>
          <small> ID: {{ bid.id }} </small>
          <v-divider vertical />
          <i> {{ bid.status }} </i>
        </v-list-item-title>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: 'SolicitudesBar',
  props: {
    bids: {
      type: Array,
      default: () => [],
    },
  },
}
</script>
