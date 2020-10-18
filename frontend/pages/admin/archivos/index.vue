<template>
  <v-card>
    <v-toolbar>
      <v-toolbar-title> Archivos </v-toolbar-title>
    </v-toolbar>

    <v-card-text>
      <v-container>
        <v-row>
          <v-col v-for="file in files" :key="file.id" cols="4">
            <v-card class="mx-auto">
              <v-img :src="getIcon(file.attachment)" height="200px" :alt="file.attachment" />

              <v-card-title>
                {{ file.attachment.split('/').pop() }}
              </v-card-title>

              <v-card-subtitle> {{ file.type_verbose_name }} (id: {{ file.id }}) </v-card-subtitle>

              <v-card-actions>
                <v-btn icon @click="file.show = !file.show">
                  <v-icon>{{ file.show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
                </v-btn>

                <v-btn icon target="_blank" :href="getSource(file.attachment)">
                  <v-icon>mdi-download</v-icon>
                </v-btn>

                <v-spacer />

                <delete-button @click="deleteFile(file.id)" />
              </v-card-actions>

              <v-expand-transition>
                <div v-show="file.show">
                  <v-divider></v-divider>

                  <v-card-text>
                    <v-textarea v-model="file.description" label="Observaciones" />
                    <v-btn block color="success" @click="updateFile(file.id, 'description', file.description)">
                      Salvar
                    </v-btn>
                  </v-card-text>
                </div>
              </v-expand-transition>
            </v-card>
          </v-col>
        </v-row>
      </v-container>

      <div class="text-center">
        <v-pagination v-model="page" :length="Math.ceil(total / 9)" @input="refresh" />
      </div>
    </v-card-text>
  </v-card>
</template>

<script>
import isImage from 'is-image'
import DeleteButton from '~/components/buttons/deleteButton'
const XLSX_EXTS = [
  'xlsx',
  'xlsb',
  'xlsm',
  'xls',
  'xml',
  'csv',
  'txt',
  'ods',
  'fods',
  'uos',
  'sylk',
  'dif',
  'dbf',
  'prn',
  'qpw',
  '123',
  'wb*',
  'wq*',
  'html',
  'htm',
]
export default {
  components: { DeleteButton },
  data() {
    return {
      loading: false,

      files: [],
      total: 0,
      page: 1,
    }
  },
  async mounted() {
    await this.refresh()
  },
  methods: {
    async refresh() {
      this.loading = true
      const data = await this.$axios.$get(`users/paginated_attachments/?page=${this.page}&page_size=9`)
      this.total = data.count
      this.files = data.results.map((f) => ({ ...f, show: false }))
      this.loading = false
    },
    async updateFile(fileId, field, value) {
      await this.$axios.$patch(`users/paginated_attachments/${fileId}/`, { [field]: value })
      await this.refresh()
    },
    deleteFile(fileId) {
      this.$swal({
        title: `Eliminar archivo ${fileId}?`,
        text: 'Una vez borrado, no podrás recuperar este archivo!',
        icon: 'warning',
        buttons: true,
        dangerMode: true,
      }).then((willDelete) => {
        if (willDelete) {
          this.$axios.$delete(`users/paginated_attachments/${fileId}/`).then(() => {
            this.$swal({
              title: 'Archivo eliminado!',
              icon: 'success',
            })
            this.refresh()
          })
        }
      })
    },
    getSource(fileUrl) {
      return fileUrl.replace('http://localhost:8001', 'https://areaclientes.gestiongroup.es')
    },
    getIcon(fileUrl) {
      fileUrl = this.getSource(fileUrl)
      if (isImage(fileUrl)) {
        return fileUrl
      } else if (XLSX_EXTS.includes(fileUrl.split('.').pop())) {
        return 'https://cdn.iconscout.com/icon/free/png-512/microsoft-excel-4-722715.png'
      } else if (fileUrl.endsWith('pdf')) {
        return 'https://cdn.iconscout.com/icon/premium/png-512-thumb/adobe-acrobat-pdf-file-document-50769.png'
      } else {
        return 'https://www.summitcl.com/wp-content/uploads/2019/03/2109135.png'
      }
    },
  },
}
</script>
