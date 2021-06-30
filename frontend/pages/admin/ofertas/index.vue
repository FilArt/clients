<template>
  <v-card>
    <v-snackbar v-model="actionsSnackbar" :timeout="-1" :value="true" color="deep-purple accent-4" elevation="24">
      <v-row align="center">
        <v-col class="flex-grow-1"> Acciones con ofertas </v-col>
        <v-col class="flex-grow-0">
          <close-button @click="actionsSnackbar = false" />
        </v-col>
      </v-row>

      <v-divider />

      <v-row>
        <v-col>
          <v-btn icon color="primary" @click="editDialog = true">
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
        </v-col>
        <v-col>
          <delete-button @click="deleteRowsDialog = !deleteRowsDialog" />
        </v-col>
      </v-row>
    </v-snackbar>

    <v-dialog v-model="addNewNameDialog">
      <v-card>
        <v-card-title>Anadir nombre</v-card-title>
        <v-card-text>
          <v-form
            @submit.prevent="
              $store.commit('setNames', [newName, ...names])
              addNewNameDialog = false
            "
          >
            <v-text-field v-model="newName" label="Nuevo nombre" @input="newName = $event.toUpperCase()" />
            <v-btn color="success" type="submit"> Anadir </v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-dialog v-model="deleteRowsDialog" max-width="500">
      <v-card>
        <v-card-title>Eliminar ofertas</v-card-title>

        <v-card-text v-if="selectedRows.length">
          {{ selectedRows.map((o) => o.id).join(', ') }}
        </v-card-text>

        <v-card-actions>
          <v-btn color="error" block @click="deleteRows"> Enviar </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="editDialog" max-width="290">
      <v-card>
        <v-form
          @submit.prevent="
            save({ [fieldToEdit.field]: newValue })
            editDialog = false
          "
        >
          <v-card-title class="headline">
            Editar {{ fieldToEdit ? fieldToEdit.label.toLowerCase() : 'ofertas' }}
          </v-card-title>

          <v-card-text v-if="!fieldToEdit">
            <v-select
              v-model="fieldToEdit"
              :items="columns.filter((c) => c.field !== 'id')"
              item-text="label"
              label="Eligir campo"
              return-object
            />
          </v-card-text>

          <v-card-text v-if="fieldToEdit">
            <offer-required-fields v-if="fieldToEdit.field === 'required_fields'" v-model="newValue" />

            <v-overflow-btn
              v-else-if="fieldToEdit.field === 'name'"
              v-model="newValue"
              label="Nuevo valor"
              editable
              segmented
              :items="names"
              append-outer-icon="mdi-plus"
              @click:append-outer="addNewNameDialog = true"
            />

            <v-select
              v-else-if="fieldToEdit.filterOptions && fieldToEdit.filterOptions.filterDropdownItems"
              v-model="newValue"
              label="Nuevo valor"
              :items="
                fieldToEdit.field === 'required_fields'
                  ? requiredFieldsItems
                  : fieldToEdit.filterOptions.filterDropdownItems
              "
              :multiple="fieldToEdit.multiple"
            />

            <v-text-field v-else v-model="newValue" autofocus label="Nuevo valor" />
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>

            <v-btn color="green darken-1" icon text @click="editDialog = false">
              <v-icon>mdi-cancel</v-icon>
            </v-btn>

            <v-btn color="green darken-1" icon text type="submit">
              <v-icon>mdi-content-save</v-icon>
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card>
    </v-dialog>

    <v-toolbar>
      <v-toolbar-title> Ofertas </v-toolbar-title>

      <v-spacer />

      <v-toolbar-items>
        <v-btn nuxt to="/admin/ofertas/comparador" color="info">
          Comparador
          <v-icon>mdi-cog</v-icon>
        </v-btn>
        <v-btn nuxt to="/admin/ofertas/comercializadoras" color="warning">Comercializadoras</v-btn>

        <v-btn nuxt to="/admin/ofertas/nuevo_oferta" color="success">
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>

    <v-card-text>
      <vue-good-table
        mode="remote"
        line-numbers
        :theme="$vuetify.theme['isDark'] ? 'nocturnal' : 'black-rhino'"
        :pagination-options="{
          enabled: true,
          mode: 'pages',
          perPage: query.itemsPerPage,
          position: 'top',
          perPageDropdown: [10, 50, 100],
          dropdownAllowAll: true,
          setCurrentPage: query.page,
        }"
        :total-rows="total"
        :is-loading.sync="loading"
        :rows="rows"
        :columns="columns"
        :search-options="{ enabled: true }"
        :select-options="{
          enabled: true,
          selectOnCheckboxOnly: true, // only select when checkbox is clicked instead of the row
          selectionText: 'rows selected',
          clearSelectionText: 'clear',
          disableSelectInfo: true, // disable the select info panel on top
          selectAllByGroup: true, // when used in combination with a grouped table, add a checkbox in the header row to check/uncheck the entire group
        }"
        @on-page-change="onPageChange"
        @on-column-filter="onColumnFilter"
        @on-sort-change="onSortChange"
        @on-per-page-change="onPerPageChange"
        @on-search="onSearch"
        @on-cell-click="onCellClick"
        @on-selected-rows-change="
          selectedRows = $event.selectedRows
          actionsSnackbar = selectedRows.length > 0
        "
      >
        <template slot="table-row" slot-scope="props">
          <div v-if="props.column.field === 'description'">
            <div style="max-width: 100px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis">
              {{ props.formattedRow[props.column.field] }}
            </div>
          </div>
          <span v-else-if="props.column.field === 'company'">
            {{ companies.find((c) => c.value === props.row.company).text }}
          </span>
          <span v-else-if="props.column.field === 'required_fields'">
            {{ getRequiredFieldText(props.row[props.column.field]) }}
          </span>
          <span v-else>
            {{ props.formattedRow[props.column.field] }}
          </span>
        </template>
      </vue-good-table>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapState } from 'vuex'
import OfferRequiredFields from '@/components/selects/OfferRequiredFields'
import DeleteButton from '@/components/buttons/deleteButton'
import CloseButton from '@/components/buttons/closeButton'
import constants from '@/lib/constants'

export default {
  components: { CloseButton, DeleteButton, OfferRequiredFields },
  data() {
    const q = this.$route.query
    return {
      actionsSnackbar: false,
      deleteRowsDialog: false,
      selectedRows: [],
      newName: '',
      addNewNameDialog: false,
      editDialog: false,
      fieldToEdit: '',
      newValue: null,

      total: 0,
      timeout: null,
      loading: false,
      rows: [],
      query: {
        ...q,
        page: q.page ? parseInt(q.page) : 1,
        itemsPerPage: q.itemsPerPage ? parseInt(q.itemsPerPage) : 10,
      },
      requiredFieldsItems: [
        { value: 'photo_cif', text: 'Foto CIF' },
        { value: 'photo_dni', text: 'Foto DNI' },
        { value: 'photo_factura', text: 'Foto factura' },
        { value: 'photo_recibo', text: 'FOTO RECIBO AUTONOMO' },
        { value: 'cif', text: 'Numero CIF' },
        { value: 'dni', text: 'Numero DNI' },
        { value: 'phone', text: 'Telefono' },
        { value: 'contrato_arredamiento', text: 'CONTRATO ARREDAMIENTO/COMPRAVENTA' },
        { value: 'name_changed_doc', text: 'DOCUMENTO CAMBIO DE NOMBRE' },
        { value: 'contrato', text: 'CONTRATO' },
      ],
      columns: [
        { label: 'ID', field: 'id', filterOptions: { enabled: true } },
        {
          label: 'Activo',
          field: 'active',
          formatFn: this.booleanFormat,
          filterOptions: {
            enabled: true,
            filterDropdownItems: [
              { text: 'Si', value: true },
              { text: 'No', value: false },
            ],
          },
        },
        {
          label: 'Tipo',
          field: 'kind',
          filterOptions: {
            enabled: true,
            filterDropdownItems: [
              { text: 'Luz', value: 'luz' },
              { text: 'Gas', value: 'gas' },
            ],
          },
        },
        {
          label: 'Comers',
          field: 'company',
          formatFn: this.formatCompany,
          filterOptions: { enabled: true, filterDropdownItems: undefined },
        },
        {
          label: 'Nombre',
          field: 'name',
          width: '200px',
          filterOptions: { enabled: true, filterDropdownItems: this.names },
        },
        { label: 'Descripcion', field: 'description', sortable: false, width: '50px' },
        { label: 'P1', field: 'p1', filterOptions: { enabled: true } },
        { label: 'P2', field: 'p2', filterOptions: { enabled: true } },
        { label: 'P3', field: 'p3', filterOptions: { enabled: true } },
        { label: 'P4', field: 'p4', filterOptions: { enabled: true } },
        { label: 'P5', field: 'p5', filterOptions: { enabled: true } },
        { label: 'P6', field: 'p6', filterOptions: { enabled: true } },
        { label: 'C1', field: 'c1', filterOptions: { enabled: true } },
        { label: 'C2', field: 'c2', filterOptions: { enabled: true } },
        { label: 'C3', field: 'c3', filterOptions: { enabled: true } },
        { label: 'C4', field: 'c4', filterOptions: { enabled: true } },
        { label: 'C5', field: 'c5', filterOptions: { enabled: true } },
        { label: 'C6', field: 'c6', filterOptions: { enabled: true } },
        { label: 'Tarifa', field: 'tarif', filterOptions: { enabled: true, filterDropdownItems: this.tarifs } },
        { label: 'Potencia min', field: 'power_min', filterOptions: { enabled: true } },
        { label: 'Potencia max', field: 'power_max', filterOptions: { enabled: true } },
        { label: 'Consumo min', field: 'consumption_min', filterOptions: { enabled: true } },
        { label: 'Consumo max', field: 'consumption_max', filterOptions: { enabled: true } },
        {
          label: 'Tipo de cliente',
          field: 'client_type',
          formatFn: this.formatClientType,
          filterOptions: {
            enabled: true,
            filterDropdownItems: Object.entries(constants.clientTypes).map((items) => ({
              text: items[1],
              value: parseInt(items[0]),
            })),
          },
        },
        {
          label: 'Tipo de precio',
          field: 'is_price_permanent',
          filterOptions: { enabled: true, filterDropdownItems: ['Fijo', 'Indexado'] },
        },
        { label: 'Canal comisiones', field: 'canal_commission', filterOptions: { enabled: true } },
        { label: 'Agente comisiones', field: 'agent_commission', filterOptions: { enabled: true } },
        {
          label: 'Campos obligatorio',
          field: 'required_fields',
          sortable: false,
          width: '200px',
          multiple: true,
          filterOptions: { filterDropdownItems: this.requiredFieldsItems },
        },
      ],
    }
  },
  computed: {
    ...mapState({
      companies: (state) => state.companies.map((c) => ({ text: c.name, value: c.id })),
      tarifs: (state) => state.tarifs,
      names: (state) => state.names,
    }),
  },
  async mounted() {
    if (!this.companies.length) await this.$store.dispatch('fetchCompanies')
    await this.refresh()
    if (!this.names.length) await this.$store.dispatch('fetchNames')
    this.columns = this.columns.map((column) => {
      if (column.field === 'company') {
        column.filterOptions.filterDropdownItems = this.companies
      } else if (column.field === 'tarif') {
        column.filterOptions.filterDropdownItems = constants.tarifs.concat(constants.tarifsGas)
      } else if (column.field === 'name') {
        column.filterOptions.filterDropdownItems = this.names
      }
      return column
    })
  },
  methods: {
    async deleteRows() {
      this.loading = true
      try {
        await this.$axios.$post('calculator/admin_offers/bulk_delete/', { ids: this.selectedRows.map((r) => r.id) })
        this.deleteRowsDialog = false
        this.updateParams({ page: 1 })
        await this.refresh()
      } finally {
        this.loading = false
      }
    },
    updateParams(newProps) {
      if (this.loading) return
      this.loading = true
      const query = Object.entries(Object.assign({}, this.query, newProps)).reduce(
        (a, [k, v]) => (v ? ((a[k] = v), a) : a),
        {},
      )
      this.query = query
      this.$router
        .replace({ query })
        .then(() => this.refresh())
        .catch(() => (this.loading = false))
    },
    onSearch(opts) {
      this.updateParams({ search: opts.searchTerm, page: 1 })
    },
    onPageChange(params) {
      this.updateParams({ page: params.currentPage })
    },
    onSortChange(params) {
      let ordering = params[0]
      ordering = ordering.type === 'asc' ? `-${ordering.field}` : ordering.field
      this.updateParams({ ordering })
    },
    onPerPageChange(params) {
      this.updateParams({ itemsPerPage: params.currentPerPage, page: 1 })
    },
    onColumnFilter(params) {
      this.updateParams({ ...params.columnFilters, page: 1 })
    },
    async refresh() {
      const fullPath = this.$route.fullPath
      let getParamsString = fullPath.includes('?') ? fullPath.split('?')[1] : 'page=1&itemsPerPage=10'
      try {
        const data = await this.$axios.$get(`calculator/admin_offers/?${getParamsString}`)
        this.total = data.count
        this.rows = data.results
      } catch (e) {
        console.error(e)
      } finally {
        this.loading = false
      }
    },

    // hueta
    getRequiredFieldText(values) {
      const str = this.requiredFieldsItems
        .filter((i) => values.includes(i.value))
        .map((i) => i.text)
        .join(', ')
      const len = 17
      return str.length > len ? str.substr(0, len) + '...' : str
    },
    onCellClick({ row, column }) {
      this.selectedRows = [row]
      this.fieldToEdit = column
      this.newValue = row[column.field]
      this.editDialog = true
    },
    async save(data) {
      for await (const row of this.selectedRows) {
        const id = row.id
        try {
          await this.$axios.$patch(`calculator/admin_offers/${id}/`, data)
        } catch (e) {
          const err = JSON.stringify(e.response.data)
          await this.$swal({ title: 'Error', text: err, icon: 'error' })
        }
      }
      await this.refresh()
      this.fieldToEdit = this.newValue = null
    },
    formatClientType: (val) => constants.clientTypes[val],
    formatCompany(id) {
      return this.companies.find((company) => company.value === id).text
    },
    booleanFormat(val) {
      return val ? 'Si' : 'No'
    },
  },
}
</script>
