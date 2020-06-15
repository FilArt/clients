<template>
  <v-card>
    <v-card-title>
      <p class="flex-grow-1">Buy offer {{ bid.id }}</p>
      <close-button @click="close" />
    </v-card-title>

    <v-card-text>
      <v-form @submit.prevent="submit" novalidate>
        <v-checkbox
          v-model="form.change_of_name"
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
          v-model="form.name"
          :label="isIndividual ? 'Nombre/razon social' : 'Nombre y apellido'"
          hint=""
        />

        <v-text-field
          v-if="!isIndividual"
          v-model="form.cif_dni"
          label="CIF/DNI"
        />

        <v-text-field
          v-if="!isIndividual"
          v-model="form.legal_representative"
          label="Representante legal"
        />

        <v-text-field v-model="form.dni" label="DNI" />

        <phone-field v-model="form.phoneMobile" label="Telefono mobil" />

        <phone-field v-model="form.phoneCity" label="Telefono pijo" />

        <email-field v-model="form.email" />

        <v-text-field v-model="form.iban" label="IBAN" />

        <v-text-field v-model="form.cups" label="CUPS LUZ" />

        <v-text-field
          v-model="form.power"
          label="Potencia contractada"
          type="number"
        />

        <v-text-field v-model="form.province" label="Provincia" />
        <v-text-field v-model="form.region" label="Poblacion" />
        <v-text-field
          v-model="form.postalcode"
          label="Codigo postal"
          type="number"
        />
        <v-text-field v-model="form.address" label="Direccion" />

        <v-file-input v-model="files.photo_factura" label="Foto factura" />
        <v-file-input v-model="files.photo_dni1" label="Foto dni anverso" />
        <v-file-input v-model="files.photo_dni2" label="Foto dni reverso" />

        <v-file-input
          v-if="!isIndividual"
          v-model="files.photo_cif1"
          label="Foto cif anverso"
        />
        <v-file-input
          v-if="!isIndividual"
          v-model="files.photo_cif2"
          label="Foto cif reverso"
        />
        <v-file-input
          v-if="!isIndividual"
          v-model="files.photo_autonomo"
          label="Foto autonomo"
        />

        <submit-button block label="Buy" />
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
const defaultForm = {
  power: null,
  email: null,
  phoneMobile: null,
  phoneCity: null,
  name: null,
  cups: null,
  change_of_name: false,
  cif_dni: null,
  legal_representative: null,
  dni: null,
  iban: null,
  province: null,
  region: null,
  postalcode: null,
  address: null,
}
export default {
  components: {
    EmailField: () => import('~/components/fields/emailField'),
    PhoneField: () => import('~/components/fields/phoneField'),
    CloseButton: () => import('~/components/buttons/closeButton'),
    SubmitButton: () => import('~/components/buttons/submitButton'),
  },
  data() {
    return {
      form: defaultForm,
      files: {
        photo_factura: null,
        photo_dni1: null,
        photo_dni2: null,
        photo_cif1: null,
        photo_cif2: null,
        photo_autonomo: null,
      },
      error: {},
    }
  },
  async asyncData({ route }) {
    return {
      bid: { id: route.query.bid },
      isIndividual: route.query.isIndividual === 'true',
    }
  },
  methods: {
    submit() {
      this.$axios
        .$post('cards', { bid: this.bid.id, ...{ data: this.form } })
        .then((data) => {
          this.$swal({
            title: 'Created',
            icon: 'success',
          })
            .catch((e) => {
              this.error = e.response.data
            })
            .then(() => {
              this.close()
            })
        })
    },
    close() {
      this.$router.push(`/bids/${this.bid.id}`)
    },
  },
}
</script>
