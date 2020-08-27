<template>
  <v-card>
    <v-card-text class="text-center">
      <div class="text-h4">Utiliza nuestra herramienta de selección de ofertas.</div>

      <div class="text-h6">
        Para utilizar el comparador, necesitará su factura de luz actual. Nuestro comparador realizará un cálculo para
        todas las ofertas disponibles en nuestra base de datos y lo ayudará a elegir la mejor oferta para usted.
      </div>
    </v-card-text>

    <v-card-text>
      <calculator />
    </v-card-text>
  </v-card>
</template>
<script>
import Calculator from '~/components/forms/Calculator'
export default {
  components: { Calculator },
}
</script>
