<template>
  <v-dialog v-model="dialog" max-width="500" :transition="false">
    <template v-slot:activator="{ on }">
      <v-btn :color="color" v-on="on">
        {{ label ? label : 'Anadir nuevo suministro' }}
        <v-icon v-if="punto" color="error" right @click.stop="puntoDeleted">
          mdi-trash-can-outline
        </v-icon>
      </v-btn>
    </template>
    <v-card>
      <v-card-title>
        <p class="flex-grow-1">
          {{ label ? label : 'Nuevo punto suministro' }}
        </p>
        <close-button @click="dialog = false" />
      </v-card-title>

      <v-card-text>
        <v-form @submit.prevent="addPunto">
          <v-radio-group v-model="newPunto.category" label="Seleccione categoría de cliente" mandatory>
            <v-radio
              v-for="category in categories"
              :key="category.value"
              :label="category.name"
              :value="category.value"
            />
          </v-radio-group>

          <div v-for="field in fields" :key="field.value">
            <company-select v-if="field.value === 'company_luz' && admin" v-model="newPunto.company_luz" />

            <v-autocomplete
              v-else-if="field.value === 'province'"
              v-model="newPunto.province"
              :label="field.name"
              :hint="field.hint"
              :name="field.value"
              prepend-icon="mdi-city"
              :items="cities"
              :error-messages="errors[field.value]"
            />

            <v-text-field
              v-else
              v-show="
                [
                  'company_luz',
                  'category',
                  'name',
                  'c1',
                  'c2',
                  'c3',
                  'p1',
                  'p2',
                  'p3',
                  'company_gas',
                  'last_time_company_luz_changed',
                  'last_time_company_gas_changed',
                  'cups_luz',
                  'cups_gas',
                  'tarif_luz',
                  'tarif_gas',
                  'consumo_annual_luz',
                  'consumo_annual_gas',
                ].includes(field.value)
                  ? admin
                  : true
              "
              v-model="newPunto[field.value]"
              class="pa-3"
              :prepend-icon="fieldIcons[field.value]"
              :label="field.name"
              :hint="field.hint"
              :name="field.value"
              :error-messages="errors[field.value]"
            />
          </div>

          <v-row v-for="fileField in fileFields" :key="fileField.name" align="center" class="flex-wrap">
            <template
              v-if="
                !(
                  (['cif1', 'recibo1'].includes(fileField.name) && newPunto.category === 'physical') ||
                  (newPunto.category === 'autonomous' && fileField.name === 'cif1') ||
                  (newPunto.category === 'business' && fileField.name === 'recibo1')
                )
              "
            >
              <v-col>
                <v-file-input
                  v-model="files[fileField.name]"
                  accept="image/*"
                  :label="fileField.label"
                  :error-messages="fileErrors[fileField.name]"
                />
              </v-col>
              <v-col
                v-for="attachment in attachments.filter((a) => a.attachment_type === fileField.name)"
                :key="attachment.id"
              >
                <v-chip
                  close
                  link
                  exact
                  target="_blank"
                  :href="attachment.attachment"
                  @click:close="deleteAttachment(attachment.id)"
                >
                  {{ attachment.type_verbose_name }}
                </v-chip>
              </v-col>
            </template>
          </v-row>

          <submit-button :label="punto ? 'Guardar' : 'Anadir nuevo punto suministro'" block />
        </v-form>
      </v-card-text>
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
      newPunto: this.punto || {},
      errors: {},
      attachments: (this.punto || {}).attachments || [],
      fieldIcons: {
        address: 'mdi-map-marker',
        iban: 'mdi-bank',
      },
      fileFields: [
        {
          name: 'factura',
          label: 'Foto factura actual (anverso)',
        },
        {
          name: 'factura_1',
          label: 'Foto factura actual (reverso)',
        },
        {
          name: 'dni1',
          label: 'Foto DNI (anverso)',
        },
        {
          name: 'dni2',
          label: 'Foto DNI (reverso)',
        },
        {
          name: 'cif1',
          label: 'Foto CIF',
        },
        {
          name: 'recibo1',
          label: 'Foto recibo de Autónomo',
        },
      ],
      files: {
        factura: null,
        factura_1: null,
        dni1: null,
        dni2: null,
        cif1: null,
      },
      fileErrors: {},
    }
  },
  computed: {
    admin() {
      return this.$auth.user.role === 'admin'
    },
    fields() {
      return this.$store.state.puntoHeaders
    },
    categories() {
      return this.$store.state.puntoCategories.filter((cat) => {
        return !(this.offerClientType === 1 && cat.value === 'physical')
      })
    },
    cities() {
      return this.$store.state.cities
    },
  },
  watch: {
    punto: {
      handler: function (val) {
        this.newPunto = val
      },
    },
  },
  async mounted() {
    if (!this.fields || !this.fields.length) {
      this.$store.commit('setPuntoHeaders', await this.$axios.$get('/users/puntos/get_headers/'))
    }
    if (this.punto) {
      this.newPunto = this.punto
    }
    if (!this.categories || !this.categories.length) {
      this.$store.commit('setPuntoCategories', await this.$axios.$get('/users/puntos/get_categories/'))
    }
    if (!this.cities || !this.cities.length) {
      this.$store.commit('setCities', await this.$axios.$get('/users/puntos/get_cities/'))
    }
  },
  methods: {
    deleteAttachment(attachmentId) {
      this.$swal({
        title: `Borrar el archivo adjunto ${attachmentId}?`,
        text: '¡Una vez borrado, no podrás recuperar esto!',
        icon: 'warning',
        buttons: true,
        dangerMode: true,
      }).then((willDelete) => {
        if (willDelete) {
          this.$axios.$delete(`users/attachments/${attachmentId}/`).then(() => {
            this.$swal({
              title: 'Solicitud eliminada!',
              icon: 'success',
            })
            this.attachments = this.attachments.filter((a) => a.id !== attachmentId)
          })
        }
      })
    },
    async loadFiles(puntoId) {
      for await (let fileKey of Object.keys(this.files)) {
        const file = this.files[fileKey]
        if (!file) continue
        const form = new FormData()
        form.append('attachment_type', fileKey)
        form.append('attachment', file)
        form.append('punto', puntoId)
        try {
          await this.$axios.$post('/users/attachments/', form)
        } catch (e) {
          this.fileErrors[fileKey] = e.response.data
        }
      }
    },
    async addPunto() {
      if (this.punto) {
        try {
          await this.$axios.$patch(`/users/puntos/${this.punto.id}/`, this.newPunto)
        } catch (e) {
          this.errors = e.response.data
          return
        }
        await this.loadFiles(this.punto.id)
        if (Object.keys(this.fileErrors).length) return
        this.$emit('fetch-puntos')
      } else {
        try {
          const punto = await this.$axios.$post('/users/puntos/', {
            ...this.newPunto,
            bid: this.bidId,
          })
          await this.loadFiles(punto.id)
          if (Object.keys(this.fileErrors).length) return
          this.$emit('fetch-puntos')
        } catch (e) {
          this.errors = e.response.data
          if (this.errors.profileNotFilled) {
            await this.$swal({
              title: 'Por favor, complete su perfil por completo.',
              text: 'Para comenzar el proceso de contratación, debe completar su perfil.',
              icon: 'warning',
            })
            await this.$router.push('/profile')
          }
          return
        }
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
