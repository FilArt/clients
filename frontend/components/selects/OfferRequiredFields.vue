<template>
  <v-select
    v-model="modelValue"
    label="Campos obligatorio"
    :items="requiredFieldsItems"
    multiple
    @input="$emit('input', $event)"
  />
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
      modelValue: this.value,
      requiredFieldsItems: [
        { value: 'photo_cif', text: 'Foto CIF' },
        { value: 'photo_dni', text: 'Foto DNI' },
        { value: 'photo_factura', text: 'Foto factura' },
        { value: 'photo_recibo', text: 'Foto recibo autonomo' },
        { value: 'cif', text: 'Numero CIF' },
        { value: 'dni', text: 'Numero DNI' },
        { value: 'phone', text: 'Telefono' },
        { value: 'contrato_arredamiento', text: 'Contrato arredamiento/compraventa' },
        { value: 'name_changed_doc', text: 'Documento cambio de nombre' },
        { value: 'contrato', text: 'Contrato' },
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
