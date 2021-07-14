<template>
  <v-card>
    <v-card-title>Creador de propuesta</v-card-title>
    <v-card-text>
      <calculator creador />
    </v-card-text>
  </v-card>
</template>
<script>
import Calculator from '../components/forms/Calculator.vue'
export default {
  components: {
    Calculator,
  },
}
</script>
