<template>
  <calculator-details :offer="offer" />
</template>

<script>
import CalculatorDetails from '@/components/CalculatorDetails'
export default {
  name: 'Offer',
  components: { CalculatorDetails },
  data() {
    return {
      offer: null,
    }
  },
}
</script>
