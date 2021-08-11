<template>
  <v-dialog v-model="dialog" max-width="750px">
    <template v-slot:activator="{ on }">
      <v-btn :color="color" v-on="on">
        <v-icon v-if="!punto" left :color="color">mdi-plus</v-icon>
        {{ punto ? punto.name : 'Añadir' }}
      </v-btn>
    </template>

    <add-punto
      :user-id="userId"
      :closeable="closeable"
      :color="color"
      :offer-client-type="offerClientType"
      :label="label"
      :punto="punto"
      :bid="bid"
      @close="dialog = false"
      @punto-updated="
        dialog = false
        $emit('punto-updated')
      "
      @punto-deleted="
        dialog = false
        $emit('punto-updated')
      "
      @punto-added="
        dialog = false
        $emit('punto-added', $event)
      "
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
    bid: {
      type: Object,
      default: () => null,
    },
    color: {
      type: String,
      default: 'success',
    },
    label: {
      type: [String, Number],
      default: null,
    },
    userId: {
      type: Number,
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
