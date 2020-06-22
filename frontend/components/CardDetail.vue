<template>
  <v-card v-if="card">
    <v-card-text>
      <v-card>
        <v-checkbox
          v-model="card.change_of_name"
          label="Cambio de nombre"
          hint="Hint"
          persistent-hint
          :items="[
            {
              text: 'Si',
              value: true,
            },
            {
              text: 'No',
              value: false,
            },
          ]"
        />
        <v-text-field
          v-model="card.name"
          :label="isIndividual ? 'Nombre/razon social' : 'Nombre y apellido'"
          hint=""
        />

        <v-text-field
          v-if="!isIndividual"
          v-model="card.cif_dni"
          label="CIF/DNI"
        />

        <v-text-field
          v-if="!isIndividual"
          v-model="card.legal_representative"
          label="Representante legal"
        />

        <v-text-field v-model="card.dni" label="DNI" />

        <phone-field v-model="card.phoneMobile" label="Telefono mobil" />

        <phone-field v-model="card.phoneCity" label="Telefono pijo" />

        <email-field v-model="card.email" />

        <v-text-field v-model="card.iban" label="IBAN" />

        <v-text-field v-model="card.cups" label="CUPS LUZ" />

        <v-text-field
          v-model="card.power"
          label="Potencia contractada"
          type="number"
        />

        <v-text-field v-model="card.province" label="Provincia" />
        <v-text-field v-model="card.region" label="Poblacion" />
        <v-text-field
          v-model="card.postalcode"
          label="Codigo postal"
          type="number"
        />
        <v-text-field v-model="card.address" label="Direccion" />
      </v-card>
    </v-card-text>
  </v-card>
</template>

<script>
import PhoneField from '~/components/fields/phoneField'
import EmailField from '~/components/fields/emailField'
export default {
  name: 'CardDetail',
  components: { EmailField, PhoneField },
  props: {
    card: {
      type: Object,
      default: () => null,
    },
  },
  computed: {
    isIndividual() {
      return false
    },
    headers() {
      return Object.keys(this.card.data).map((header) => {
        return {
          text: header,
          value: header,
        }
      })
    },
  },
}
</script>
