<template>
  <v-list nav dense>
    <v-list-group v-for="punto in puntos" :key="punto.id">
      <template v-slot:activator>
        <v-toolbar dense>
          <v-toolbar-title>Punto suministro (id: {{ punto.id }})</v-toolbar-title>
        </v-toolbar>
      </template>

      <v-card class="d-flex flex-wrap">
        <v-card v-for="group in groups" :key="group.text" flat class="pa-3 mx-auto">
          <v-card-title>{{ group.text }}</v-card-title>

          <div v-for="header in group.headers" :key="header.value">
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
          </div>

          <v-flex v-if="group.text === 'Documentacion' && punto.attachments.length">
            <v-chip
              v-for="attachment in punto.attachments"
              :key="attachment.id"
              link
              exact
              target="_blank"
              :href="attachment.attachment"
            >
              {{ attachment.type_verbose_name }}
            </v-chip>
          </v-flex>

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
                        <span class="title headline"> Upload file </span>
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
        </v-card>
      </v-card>
    </v-list-group>
  </v-list>
</template>

<script>
import constants from '@/lib/constants'

export default {
  name: 'PuntosList',
  components: {
    CompanySelect: () => import('~/components/selects/CompanySelect'),
  },
  props: {
    puntos: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    const puntoValues = Object.values(constants.puntoFields)

    return {
      attachmentsItems: [
        { value: 'factura', text: 'Factura' },
        { value: 'factura_1', text: 'Factura reverso' },
        { value: 'dni1', text: 'DNI' },
        { value: 'dni2', text: 'DNI reverse side' },
        { value: 'cif1', text: 'CIF' },
        { value: 'cif2', text: 'CIF reverse side' },
        { value: 'recibo1', text: 'Recibo de Autónomo' },
        { value: 'repr_legal', text: 'Foto DNI Representante Legal' },
        { value: 'name_changed', text: 'Cambio de nombre' },
        { value: 'arredamiento', text: 'Contrato arredamiento' },
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
