<template>
  <v-row class="flex-wrap" align="top" justify="center">
    <v-col class="flex-grow-0">
      <solicitudes-bar :user-id="user.id" :bids="user.bids" @bid-added="$emit('bid-added')" />
    </v-col>

    <v-col class="flex-grow-1">
      <v-card>
        <v-card-text>
          <tramitacion :facturacion="facturacion" @tramitate="$emit('tramitate')" />
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'SolicitudesProcess',
  components: {
    SolicitudesBar: () => import('@/components/support/SolicitudesBar'),
    Tramitacion: () => import('@/components/support/Tramitacion'),
  },
  props: {
    user: {
      type: Object,
      default: () => null,
    },
    facturacion: {
      type: Boolean,
      default: false,
    },
  },
}
</script>
