<template>
  <v-card>
    <v-toolbar>
      <v-toolbar-title> Ofertas </v-toolbar-title>

      <v-spacer />

      <v-toolbar-items>
        <v-btn nuxt to="/admin/ofertas/nuevo_oferta" color="success">
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>

    <v-card-text>
      <v-dialog v-model="editDialog" max-width="290">
        <v-card>
          <v-form
            @submit.prevent="
              save(rowToEdit.id, { [fieldToEdit.field]: newValue })
              editDialog = false
            "
          >
            <v-card-title class="headline">Editar {{ fieldToEdit.field }}</v-card-title>

            <v-card-text>
              <offer-required-fields v-if="fieldToEdit.field === 'required_fields'" v-model="newValue" />

              <v-select
                v-else-if="fieldToEdit.filterOptions && fieldToEdit.filterOptions.filterDropdownItems"
                v-model="newValue"
                :items="
                  fieldToEdit.field === 'required_fields'
                    ? requiredFieldsItems
                    : fieldToEdit.filterOptions.filterDropdownItems
                "
                :multiple="fieldToEdit.multiple"
              />

              <v-text-field v-else v-model="newValue" autofocus />
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
      <vue-good-table
        mode="remote"
        line-numbers
        :theme="$vuetify.theme.isDark ? 'nocturnal' : 'black-rhino'"
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
        @on-page-change="onPageChange"
        @on-column-filter="onColumnFilter"
        @on-sort-change="onSortChange"
        @on-per-page-change="onPerPageChange"
        @on-search="onSearch"
        @on-cell-click="onCellClick"
      >
        <template slot="table-row" slot-scope="props">
          <span v-if="props.column.field === 'description'">
            <div style="max-width: 100px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis">
              {{ props.formattedRow[props.column.field] }}
            </div>
          </span>
          <span v-else-if="props.column.field === 'company'">
            {{ props.row.company.name }}
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

export default {
  components: { OfferRequiredFields },
  data() {
    const q = this.$route.query
    return {
      editDialog: false,
      fieldToEdit: '',
      newValue: null,
      rowToEdit: null,

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
      ],
      columns: [
        { label: 'ID', field: 'id', filterOptions: { enabled: true } },
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
        { label: 'C1', field: 'c1', filterOptions: { enabled: true } },
        { label: 'C2', field: 'c2', filterOptions: { enabled: true } },
        { label: 'C3', field: 'c3', filterOptions: { enabled: true } },
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
            filterDropdownItems: [
              { text: 'J', value: 1 },
              { text: 'F', value: 0 },
            ],
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
    if (!this.tarifs.length) await this.$store.dispatch('fetchTarifs')
    if (!this.names.length) await this.$store.dispatch('fetchNames')
    this.columns = this.columns.map((column) => {
      if (column.field === 'company') {
        column.filterOptions.filterDropdownItems = this.companies
      } else if (column.field === 'tarif') {
        column.filterOptions.filterDropdownItems = this.tarifs
      } else if (column.field === 'name') {
        column.filterOptions.filterDropdownItems = this.names
      }
      return column
    })
    this.refresh()
  },
  methods: {
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
    refresh() {
      const fullPath = this.$route.fullPath
      let getParamsString = fullPath.includes('?') ? fullPath.split('?')[1] : 'page=1&itemsPerPage=10'
      this.$axios
        .$get(`calculator/admin_offers/?${getParamsString}`)
        .then((data) => {
          this.total = data.count
          this.rows = data.results
        })
        .catch((e) => console.error(e))
        .finally(() => (this.loading = false))
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
      this.fieldToEdit = column
      this.rowToEdit = row
      this.newValue = row[column.field]
      this.editDialog = true
    },
    async save(id, data) {
      try {
        await this.$axios.$patch(`calculator/admin_offers/${id}/`, data)
        await this.refresh()
      } catch (e) {
        const err = JSON.stringify(e.response.data)
        await this.$swal({ title: 'Error', text: err, icon: 'error' })
      }
    },
    formatClientType: (val) => (val === 0 ? 'F' : 'J'),
    formatCompany(id) {
      return this.companies.find((company) => company.value === id).text
    },
  },
}
</script>
