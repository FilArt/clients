<template>
  <v-card :to="to" class="pa-1">
    <v-row align="center">
      <v-col cols="1">{{ bid.id }}</v-col>
      <v-col cols="2">{{ bid.status }}</v-col>
      <v-col cols="2">{{ bid['fecha_firma'] }}</v-col>
      <v-col cols="1">Doc: {{ doc }}</v-col>
      <v-col cols="2">Llamada: {{ call }}</v-col>
      <v-col cols="2">Scoring: {{ scoring }}</v-col>
      <v-col v-if="bid['offer_status_accesible']" cols="2">Estado de oferta: {{ offer_status }}</v-col>
    </v-row>
  </v-card>
</template>

<script>
const BOOL_TRUE = '✅'
const BOOL_FALSE = '❌'
export default {
  name: 'BidDetail',
  props: {
    bid: {
      type: Object,
      default: () => ({ status: 'ERROR' }),
    },
    to: {
      type: String,
      default: null,
    },
  },
  computed: {
    doc() {
      return this.bid.doc ? BOOL_TRUE : BOOL_FALSE
    },
    call() {
      return this.bid.call ? BOOL_TRUE : BOOL_FALSE
    },
    scoring() {
      return this.bid.scoring ? BOOL_TRUE : BOOL_FALSE
    },
    offer_status() {
      return this.bid.offer_status ? BOOL_TRUE : BOOL_FALSE
    },
  },
}
</script>
