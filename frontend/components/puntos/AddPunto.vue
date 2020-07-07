<template>
  <v-dialog v-model="dialog">
    <template v-slot:activator="{ on }">
      <v-btn v-on="on" :color="color"
        >{{ label ? label : 'Add nuevo suministro' }}
        <v-icon color="error" v-if="punto" right @click.stop="puntoDeleted">
          mdi-trash-can-outline
        </v-icon>
      </v-btn>
    </template>
    <v-card>
      <v-card-title>
        <p class="flex-grow-1">
          {{ label ? label : 'Nuevo punto' }}
        </p>
        <close-button @click="dialog = false" />
      </v-card-title>
      <div class="d-flex flex-wrap">
        <div v-for="field in fields" :key="field.value">
          <company-select
            v-show="admin"
            v-if="['company_gas_id', 'company_luz_id'].includes(field.value)"
            v-model="newPunto[field.value.replace('_id', '')]"
            :label="field.name"
          />
          <v-text-field
            v-else
            v-model="newPunto[field.value]"
            class="pa-3"
            clearable
            :label="field.name"
            :error-messages="errors[field.value]"
            v-show="
              [
                'last_time_company_luz_changed',
                'last_time_company_gas_changed',
                'cups_gas',
                'tarif_gas',
                'consumo_annual_luz',
                'consumo_annual_gas',
              ].includes(field.value)
                ? admin
                : true
            "
          />
        </div>
      </div>

      <submit-button
        :label="punto ? 'Guardar' : 'Anadir suministro'"
        block
        @click="addPunto"
      />
    </v-card>
  </v-dialog>
</template>
<script>
export default {
  name: 'AddPunto',
  components: {
    SubmitButton: () => import('~/components/buttons/submitButton'),
    CloseButton: () => import('~/components/buttons/closeButton'),
    CompanySelect: () => import('~/components/selects/CompanySelect'),
  },
  props: {
    color: {
      type: [String],
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
      fields: [],
      newPunto: this.punto || {},
      errors: {},
    }
  },
  async created() {
    await this.refresh()
    if (this.punto) {
      this.newPunto = this.punto
    }
  },
  watch: {
    punto: {
      handler: function (val) {
        this.newPunto = val
      },
    },
  },
  computed: {
    admin() {
      return this.$auth.user.role === 'admin'
    },
  },
  methods: {
    async refresh() {
      this.fields = await this.$axios.$get('/cards/puntos/get_headers/')
    },
    async addPunto() {
      if (this.punto) {
        try {
          await this.puntoEdited()
        } catch (e) {
          this.errors = e.response.data
          return
        }

        this.$emit('punto-edited', { punto: this.newPunto, id: this.punto.id })
      } else {
        this.$emit('punto-created', { punto: this.newPunto })
      }
      this.newPunto = {}
      this.dialog = false
    },
    puntoDeleted() {
      const id = this.punto.id
      this.$swal({
        title: `Borrar el punto ${id}?`,
        text: '¡Una vez borrado, no podrás recuperar esto!',
        icon: 'warning',
        buttons: true,
        dangerMode: true,
      }).then((willDelete) => {
        if (willDelete) {
          this.$axios.$delete(`cards/puntos/${id}/`).then(() => {
            this.$swal({ title: 'Punto eliminada!', icon: 'success' })
            this.$emit('punto-deleted')
          })
        }
      })
    },
    async puntoEdited() {
      const id = this.punto.id
      const punto = this.newPunto
      const updatedCard = await this.$axios.$patch(
        `/cards/puntos/${id}/`,
        punto
      )
      await this.$swal({
        title: 'punto ' + id + ' изменено',
        icon: 'success',
      })
      this.$emit('punto-edited')
    },
  },
}
</script>
