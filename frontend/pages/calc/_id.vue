<template>
  <v-container>
    <v-btn icon color="error" @click="$router.back()">
      <v-icon>mdi-arrow-left</v-icon>
    </v-btn>

    <calculator-details :offer="offer" />
  </v-container>
</template>

<script>
import CalculatorDetails from '@/components/CalculatorDetails'
export default {
  auth: 'guest',
  components: { CalculatorDetails },
  async asyncData({ $axios, route }) {
    const offer = await $axios.$get(`calculator/offers/${route.params.id}/`)
    return {
      offer,
    }
  },
}
</script>
