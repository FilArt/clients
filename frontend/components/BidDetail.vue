<template>
  <v-row align="center">
    <v-col class="flex-grow-0">{{ bid.id }}</v-col>
    <v-col>{{ bid.status }}</v-col>
    <v-col>FR: {{ bid['created_at'] }}</v-col>
    <template v-if="mode.includes('tramitacion')">
      <v-col>Doc: {{ signs[bid.doc] }}</v-col>
      <v-col>Llamada: {{ signs[bid.call] }}</v-col>
      <v-col>Scoring: {{ signs[bid.scoring] }}</v-col>
      <v-col v-if="bid['offer_status_accesible']" cols="2">Estado de oferta: {{ signs[bid.offer_status] }}</v-col>
    </template>
    <template v-else>
      <v-col>FF: {{ bid['fecha_firma'] || '-' }}</v-col>
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
