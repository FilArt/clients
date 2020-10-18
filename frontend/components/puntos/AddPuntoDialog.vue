<template>
  <v-dialog v-model="dialog" max-width="750px">
    <template v-slot:activator="{ on }">
      <v-btn color="success" v-on="on">
        <v-icon left color="succes">mdi-plus</v-icon>
        Añadir
      </v-btn>
    </template>

    <add-punto
      :closeable="closeable"
      :color="color"
      :offer-client-type="offerClientType"
      :label="label"
      :punto="punto"
      :bid-id="bidId"
      @close="dialog = false"
      @punto-added="$emit('punto-added')"
    />
  </v-dialog>
</template>

<script>
import AddPunto from '@/components/puntos/AddPunto'
export default {
  name: 'AddPuntoDialog',
  components: { AddPunto },
  props: {
    closeable: {
      type: Boolean,
      default: false,
    },
    offerClientType: {
      type: Number,
      default: null,
    },
    bidId: {
      type: Number,
      default: 0,
    },
    color: {
      type: String,
      default: null,
    },
    label: {
      type: [String, Number],
      default: null,
    },
    punto: {
      type: Object,
      default: () => null,
    },
  },
  data() {
    return {
      dialog: false,
    }
  },
}
</script>
