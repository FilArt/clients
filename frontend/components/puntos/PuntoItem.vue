<template>
  <v-dialog v-model="puntoDialog" max-width="1500">
    <template v-slot:activator="{ on }">
      <v-list-item-title>
        <v-btn v-on="on"> (id: {{ punto.id }}) {{ punto.kind === 'luz' ? punto.cups_luz : punto.cups_gas }} </v-btn>
      </v-list-item-title>
    </template>

    <v-card>
      <v-card-title>
        <v-row align="center">
          <v-col>
            {{ punto.kind === 'luz' ? punto.cups_luz : punto.cups_gas }}
          </v-col>
          <v-col class="flex-grow-0">
            <delete-button @click="deletePunto(punto)" />
          </v-col>
          <v-col class="flex-grow-0">
            <close-button @click="puntoDialog = false" />
          </v-col>
        </v-row>

        <v-row class="flex-wrap">
          <v-col v-for="group in groups" :key="group.text" flat class="pa-3 mx-auto">
            <v-card-title>{{ group.text }}</v-card-title>

            <v-card-text v-for="header in group.headers" :key="header.value">
              <company-select
                v-if="header.value === 'company_luz'"
                :value="punto.company_luz"
                @input="
                  save({
                    id: punto.id,
                    field: 'company_luz',
                    value: $event,
                  })
                "
              />

              <v-select
                v-else-if="header.value === 'category'"
                :label="header.text"
                :items="categories"
                :value="punto.category"
                @input="save({ id: punto.id, field: 'category', value: $event })"
              />

              <v-switch
                v-else-if="header.type === 'switch'"
                v-model="punto[header.value]"
                dense
                :label="header.text"
                append-icon="mdi-content-save"
                @change="values[header.value] = $event"
                @click:append="save({ id: punto.id, field: header.value })"
              />

              <v-text-field
                v-else
                v-model="punto[header.value]"
                dense
                :label="header.text"
                append-icon="mdi-content-save"
                @input="values[header.value] = $event"
                @click:append="save({ id: punto.id, field: header.value })"
              />
            </v-card-text>

            <v-row
              v-if="group.text === 'Documentacion' && punto.attachments.length"
              align="center"
              class="flex-wrap"
              style="max-width: 500px"
            >
              <v-col>
                <v-menu v-for="attachment in punto.attachments" :key="attachment.id" offset-y>
                  <template v-slot:activator="{ on }">
                    <v-chip exact :color="getColor(attachment.id)" v-on="on">
                      {{ attachment.type_verbose_name }} - ({{ attachment.id }})
                    </v-chip>
                  </template>
                  <v-list>
                    <v-list-item link target="_blank" :href="attachment.attachment">
                      <v-list-item-title>Abrir archivo</v-list-item-title>
                    </v-list-item>
                    <v-list-item color="error" @click="deleteFile(attachment.id)">
                      <v-list-item-title>Eliminar archivo</v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu>
              </v-col>
            </v-row>

            <v-flex v-if="group.text === 'Documentacion'">
              <v-dialog v-model="uploadFileDialog" max-width="500">
                <template v-slot:activator="{ on }">
                  <v-btn icon color="success" v-on="on">
                    <v-icon>mdi-file</v-icon>
                  </v-btn>
                </template>
                <v-card>
                  <v-card-text>
                    <v-card-title>
                      <v-row>
                        <v-col>
                          <span class="title headline">Añadir archivo</span>
                        </v-col>
                        <v-col class="flex-grow-0">
                          <v-btn icon color="error" @click="uploadFileDialog = false">
                            <v-icon>mdi-close</v-icon>
                          </v-btn>
                        </v-col>
                      </v-row>
                    </v-card-title>
                    <v-form @submit.prevent="uploadFile(punto.id)">
                      <v-select v-model="fileType" :items="attachmentsItems" />
                      <v-file-input v-model="file" />
                      <v-btn type="submit" block color="success">Enviar</v-btn>
                    </v-form>
                  </v-card-text>
                </v-card>
              </v-dialog>
            </v-flex>
          </v-col>
        </v-row>
      </v-card-title>
    </v-card>
  </v-dialog>
</template>

<script>
import constants from '@/lib/constants'

export default {
  name: 'PuntoItem',
  components: {
    DeleteButton: () => import('@/components/buttons/deleteButton'),
    CloseButton: () => import('@/components/buttons/closeButton'),
    CompanySelect: () => import('~/components/selects/CompanySelect'),
  },
  props: {
    punto: {
      type: Object,
      default: () => ({}),
    },
  },
  data() {
    const puntoValues = Object.values(constants.puntoFields)

    return {
      puntoDialog: false,
      categories: [
        { text: 'Físico', value: 'physical' },
        { text: 'Autónomo', value: 'autonomous' },
        { text: 'Jurídico', value: 'business' },
      ],
      attachmentsItems: [
        { value: 'factura', text: 'Factura' },
        { value: 'factura_1', text: 'Factura reverso' },
        { value: 'dni1', text: 'DNI' },
        { value: 'dni2', text: 'DNI reverse side' },
        { value: 'cif1', text: 'CIF' },
        { value: 'recibo1', text: 'Recibo de Autónomo' },
        { value: 'repr_legal', text: 'Foto DNI Representante Legal' },
        { value: 'name_changed', text: 'Cambio de nombre' },
        { value: 'arredamiento', text: 'Contrato arredamiento' },
        { value: 'contrato', text: 'Contrato' },
      ],
      uploadFileDialog: false,
      file: null,
      fileType: null,
      loading: false,
      values: {},
      groups: puntoValues
        .map((field) => field.group.text)
        .filter(constants.onlyUnique)
        .map((groupText) => {
          return {
            text: groupText,
            headers: puntoValues.filter((field) => field.group.text === groupText),
          }
        }),
    }
  },
  methods: {
    async deletePunto(punto) {
      const willDelete = await this.$swal({
        title: `Eliminar punto ${punto.cups}?`,
        text: 'Una vez borrado, no podrás recuperar este punto!',
        icon: 'warning',
        buttons: true,
        dangerMode: true,
      })
      if (!willDelete) return
      await this.$axios.$delete(`/users/puntos/${punto.id}/`)
      this.puntoDialog = false
      this.$emit('punto-updated')
    },
    getColor(attachmentId) {
      const q = this.$route.query
      if (q.highligh_item === 'attachment' && q.highligh_item_id === String(attachmentId)) {
        return 'success'
      }
      return 'primary'
    },
    async deleteFile(fileId) {
      const willDelete = await this.$swal({
        title: `Borrar el archivo ${fileId}?`,
        text: '¡Una vez borrado, no podrás recuperar esto!',
        icon: 'warning',
        buttons: true,
        dangerMode: true,
      })
      if (!willDelete) return
      await this.$axios.$delete(`users/attachments/${fileId}/`)
      await this.$emit('punto-updated')
      await this.$swal({ title: 'Listo', icon: 'success' })
    },
    async save({ id, field, value }) {
      const data = {}
      value = value === undefined ? null : value
      data[field] = value || this.values[field]
      try {
        await this.$axios.$patch(`users/puntos/${id}/`, data)
        await this.$swal({
          title: 'Salvado',
          text: `${field.toUpperCase()} esta cambiado ${value || this.values[field] || 'null'}`,
          icon: 'success',
        })
        this.$emit('punto-updated')
      } catch (e) {
        const errorMsg = e.response.data
        await this.$swal({
          title: 'Error!',
          text: errorMsg[field] instanceof Array ? errorMsg[field].join(',') : JSON.stringify(errorMsg),
          icon: 'error',
        })
      }
    },
    uploadFile(puntoId) {
      this.loading = true
      const form = new FormData()
      form.append('punto', puntoId)
      form.append('attachment_type', this.fileType)
      form.append('attachment', this.file)
      this.$axios
        .$post(`users/attachments/`, form)
        .then(() => {
          this.uploadFileDialog = false
          this.file = null
          this.fileType = null
          this.$emit('punto-updated')
        })
        .catch((e) => this.$swal({ title: 'Error', text: JSON.stringify(e.response.data) }))
        .finally(() => (this.loading = false))
    },
  },
}
</script>
