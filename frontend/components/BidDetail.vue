<template>
  <v-row align="center">
    <v-col cols="1">{{ bid.id }}</v-col>
    <v-col cols="2">{{ bid.status }}</v-col>
    <v-col cols="1">FR: {{ bid['created_at'] }}</v-col>
    <v-col cols="1">FF: {{ bid['fecha_firma'] || '-' }}</v-col>
    <template v-if="mode.includes('tramitacion')">
      <v-col cols="1">Doc: {{ signs[bid.doc] }}</v-col>
      <v-col cols="2">Llamada: {{ signs[bid.call] }}</v-col>
      <v-col cols="2">Scoring: {{ signs[bid.scoring] }}</v-col>
      <v-col v-if="bid['offer_status_accesible']" cols="2">Estado de oferta: {{ signs[offer_status] }}</v-col>
    </template>
    <template v-else>
      <v-col>Agente: {{ bid.commission }} € ({{ signs[bid.paid] }})</v-col>
      <v-col>Canal: {{ bid.canal_commission }} € ({{ signs[bid.canal_paid] }})</v-col>
      <v-col>Fecha de cobro prevista: {{ bid.fecha_de_cobro_prevista || '-' }}</v-col>
    </template>
  </v-row>
</template>

<script>
export default {
  name: 'BidDetail',
  props: {
    bid: {
      type: Object,
      default: () => ({ status: 'ERROR' }),
    },
    mode: {
      type: String,
      default: 'tramitacion',
    },
  },
  data() {
    return {
      signs: {
        true: '✅',
        false: '❌',
        null: '⏳',
      },
    }
  },
}
</script>
