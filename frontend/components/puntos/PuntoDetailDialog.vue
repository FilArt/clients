<template>
  <v-dialog v-model="dialog" max-width="500" :transition="false">
    <template v-slot:activator="{ on }">
      <v-btn :color="color" v-on="on">
        {{ label ? label : 'Anadir nuevo suministro' }}
        <v-icon v-if="punto" color="error" right @click.stop="puntoDeleted"> mdi-trash-can-outline </v-icon>
      </v-btn>
    </template>
    <add-punto
      :offer-client-type="offerClientType"
      :bid-id="bidId"
      :color="color"
      :label="label"
      :punto="punto"
      :closeable="closeable"
      @punto-added="dialog = false"
      @close="dialog = false"
    />
  </v-dialog>
</template>
<script>
export default {
  name: 'PuntoDetailDialog',
  components: {
    AddPunto: () => import('~/components/puntos/AddPunto'),
  },
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
      default: null,
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
  methods: {
    puntoDeleted() {
      const { id } = this.punto
      this.$swal({
        title: `Borrar el punto ${id}?`,
        text: '¡Una vez borrado, no podrás recuperar esto!',
        icon: 'warning',
        buttons: true,
        dangerMode: true,
      }).then((willDelete) => {
        if (willDelete) {
          this.$axios.$delete(`users/puntos/${id}/`).then(() => {
            this.$swal({
              title: 'Punto suministro eliminada!',
              icon: 'success',
            })
            this.$emit('fetch-puntos')
          })
        }
      })
    },
  },
}
</script>
