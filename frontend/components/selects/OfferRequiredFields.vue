<template>
  <v-select v-model="modelValue" label="Campos obligatorio" :items="requiredFieldsItems" multiple />
</template>

<script>
export default {
  name: 'OfferRequiredFields',
  props: {
    value: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      modelValue: [],
      requiredFieldsItems: [
        { value: 'photo_cif', text: 'Foto CIF' },
        { value: 'photo_dni', text: 'Foto DNI' },
        { value: 'photo_factura', text: 'Foto factura' },
        { value: 'photo_recibo', text: 'FOTO RECIBO AUTONOMO' },
        { value: 'cif', text: 'Numero CIF' },
        { value: 'dni', text: 'Numero DNI' },
        { value: 'phone', text: 'Telefono' },
        { value: 'contrato_arredamiento', text: 'CONTRATO ARREDAMIENTO/COMPRAVENTA' },
        { value: 'name_changed_doc', text: 'DOCUMENTO CAMBIO DE NOMBRE' },
      ],
    }
  },
  watch: {
    value(newValue) {
      this.modelValue = newValue
    },
  },
}
</script>
