<template>
  <div>
    <v-dialog v-if="punto" v-model="puntoDialog" max-width="1500">
      <template v-slot:activator="{ on }">
        <v-list-item-title>
          <v-btn v-on="on"> (id: {{ punto.id }}) {{ punto.name }} </v-btn>
        </v-list-item-title>
      </template>

      <v-card>
        <v-card-title>
          <v-row align="center">
            <v-col>
              {{ punto.cups_luz || punto.cups_gas }}
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
                <company-select
                  v-else-if="header.value === 'company_gas'"
                  :value="punto.company_gas"
                  @input="
                    save({
                      id: punto.id,
                      field: 'company_gas',
                      value: $event,
                    })
                  "
                />

                <tarif-select
                  v-else-if="header.value === 'tarif_luz'"
                  v-model="punto[header.value]"
                  :label="header.text"
                  @input="save({ id: punto.id, field: 'tarif_luz', value: $event })"
                />
                <tarif-select
                  v-else-if="header.value === 'tarif_gas'"
                  v-model="punto[header.value]"
                  gas
                  :label="header.text"
                  @input="save({ id: punto.id, field: 'tarif_gas', value: $event })"
                />

                <client-type-select
                  v-else-if="header.value === 'client_type'"
                  :label="header.text"
                  :value="punto.client_type"
                  @input="save({ id: punto.id, field: 'client_type', value: $event })"
                />

                <v-select
                  v-else-if="header.value === 'province'"
                  :label="header.text"
                  :items="$store.state.cities"
                  :value="punto.province"
                  @input="save({ id: punto.id, field: 'province', value: $event })"
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
                  v-else-if="punto[header.value] === 'name' ? punto.is_name_changed : true"
                  v-model="punto[header.value]"
                  dense
                  :label="header.text"
                  append-icon="mdi-content-save"
                  @input="values[header.value] = $event"
                  @click:append="save({ id: punto.id, field: header.value })"
                />
                {{ punto[header.value] }}
              </v-card-text>

              <v-row
                v-if="group.text === 'Documentacion' && punto.attachments && punto.attachments.length"
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

              <v-flex v-if="$auth.user.role !== 'agent' && group.text === 'Documentacion'">
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
    <v-alert v-else type="error">No hay punto</v-alert>
  </div>
</template>

<script>
import constants from '@/lib/constants'
export default {
  name: 'PuntoItem',
  components: {
    ClientTypeSelect: () => import('@/components/selects/ClientTypeSelect'),
    DeleteButton: () => import('@/components/buttons/deleteButton'),
    CloseButton: () => import('@/components/buttons/closeButton'),
    CompanySelect: () => import('@/components/selects/CompanySelect'),
    TarifSelect: () => import('@/components/selects/TarifSelect.vue'),
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
        { value: 'anexo', text: 'Anexo' },
        { value: 'hoja', text: 'HOJA DE ACTIVACIÓN FUTURA' },
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
  async mounted() {
    await this.$store.dispatch('fetchProvinces')
  },
  methods: {
    async deletePunto(punto) {
      const willDelete = await this.$swal({
        title: `Eliminar punto ${punto.cups_luz || punto.cups_gas}?`,
        text: 'Una vez borrado, no podrás recuperar este punto!',
        icon: 'warning',
        buttons: true,
        dangerMode: true,
      })
      if (!willDelete) return
      try {
        await this.$axios.$delete(`/users/puntos/${punto.id}/`)
      } catch (e) {
        this.$swal.error(e.response && e.response.data ? JSON.stringify(e.response.data) : e)
      }
      this.$emit('punto-updated')
      await this.$router.replace({ query: null })
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
      data[field] = value === 0 ? value : value || this.values[field]
      try {
        await this.$axios.$patch(`users/puntos/${id}/`, data)
        this.$toast.global.done()
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
