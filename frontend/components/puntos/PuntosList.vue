<template>
  <v-list nav dense>
    <v-list-item v-for="punto in puntos" :key="punto.id">
      <punto-item :punto="punto" @punto-updated="$emit('punto-updated')" />
    </v-list-item>
  </v-list>
</template>

<script>
import PuntoItem from '@/components/puntos/PuntoItem'

export default {
  name: 'PuntosList',
  components: {
    PuntoItem,
  },
  props: {
    puntos: {
      type: Array,
      default: () => [],
    },
  },
}
</script>
