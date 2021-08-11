<template>
  <v-card>
    <v-card-title>
      <p class="flex-grow-1">
        {{ label ? label : 'Nuevo punto suministro' }}
      </p>
      <close-button v-if="closeable" @click="$emit('close')" />
    </v-card-title>

    <v-card-text>
      <v-form @submit.prevent="addPunto">
        <div v-for="field in puntoFields" :key="field.value">
          <v-switch
            v-if="field.value === 'is_name_changed'"
            v-model="newPunto.is_name_changed"
            label="Cambio de nombre"
          />

          <company-select v-else-if="field.value === 'company_luz' && admin" v-model="newPunto.company_luz" />

          <company-select v-else-if="field.value === 'company_gas' && admin" v-model="newPunto.company_gas" />

          <decimal-field v-else-if="isDecimal(field)" v-model="newPunto[field.value]" :label="field.text" />

          <v-autocomplete
            v-else-if="field.value === 'province'"
            v-model="newPunto.province"
            :label="field.text"
            :hint="field.hint"
            :name="field.value"
            prepend-icon="mdi-city"
            :items="cities"
            :error-messages="errors[field.value]"
          />

          <v-text-field
            v-show="field.value === 'name' ? newPunto.is_name_changed : true"
            v-else
            v-model="newPunto[field.value]"
            class="pa-3"
            :prepend-icon="field.icon"
            :label="field.text"
            :hint="field.hint"
            :name="field.value"
            :error-messages="errors[field.value]"
          />
        </div>

        <v-row v-for="fileField in fileFields" :key="fileField.name" align="center" class="flex-wrap">
          <template
            v-if="
              !(
                (['cif1', 'recibo1'].includes(fileField.name) && offerClientType === 0) ||
                (offerClientType === 2 && fileField.name === 'cif1') ||
                (offerClientType === 1 && fileField.name === 'recibo1')
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
</template>
<script>
import constants from '@/lib/constants'
const requiredFieldsMap = {
  photo_cif: ['cif1'],
  photo_dni: ['dni1', 'dni2'],
  photo_factura: ['factura', 'factura_1'],
  photo_recibo: ['recibo1'],
  name_changed_doc: ['name_changed'],
  contrato_arredamiento: ['arredamiento'],
  contrato: ['contrato'],
  cif: ['cif'],
  dni: ['dni'],
  phone: ['phone'],
}
export default {
  name: 'AddPunto',
  components: {
    SubmitButton: () => import('~/components/buttons/submitButton'),
    CloseButton: () => import('~/components/buttons/closeButton'),
    CompanySelect: () => import('~/components/selects/CompanySelect'),
    DecimalField: () => import('@/components/fields/decimalField.vue'),
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
    bid: {
      type: Object,
      default: () => null,
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
    userId: {
      type: [String, Number],
      default: () => null,
    },
  },
  data() {
    const newPunto = this.punto || {}
    return {
      newPunto,
      errors: {},
      attachments: (this.punto || {}).attachments || [],

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
    fileFields() {
      const requiredFields = (this.bid.offer.required_fields || []).map((rf) => requiredFieldsMap[rf]).flat()
      return [
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
      ].filter((fileField) => requiredFields.includes(fileField.name))
    },
    puntoFields() {
      return Object.values(constants.puntoFields)
        .filter((field) => (this.admin || !field.onlyAdmin) && field.value !== 'client_type')
        .map((field) => {
          return {
            text: field.text,
            value: field.value,
            icon: field.icon,
          }
        })
    },
    admin() {
      return this.$auth.user.role === 'admin'
    },
    cities() {
      return this.$store.state.cities
    },
    getNewPunto() {
      return {
        ...this.newPunto,
        client_type: this.offerClientType || this.bid.offer.client_type,
      }
    },
  },
  watch: {
    punto: {
      handler(val) {
        this.newPunto = val
      },
    },
  },
  async mounted() {
    if (this.punto) {
      this.newPunto = this.punto
    }
    if (!this.cities || !this.cities.length) {
      await this.$store.dispatch('fetchProvinces')
    }
  },
  methods: {
    isDecimal(field) {
      return ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'consumo_annual_gas', 'consumo_annual_luz'].includes(field.value)
    },
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
      for await (const fileKey of Object.keys(this.files)) {
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
          await this.$axios.$patch(`/users/puntos/${this.punto.id}/`, this.getNewPunto)
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
            ...this.getNewPunto,
            bid: { ...this.bid, offer: this.bid.offer.id },
            user: this.userId,
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
      this.$emit('punto-added')
    },
  },
}
</script>
