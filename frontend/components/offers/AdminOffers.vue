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
        <!-- <v-col>
          <delete-button @click="deleteRowsDialog = !deleteRowsDialog" />
        </v-col> -->
      </v-row>
    </v-snackbar>

    <!-- 
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
    </v-dialog> -->

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

      <v-toolbar-items class="align-center">
        <calculator-settings-dialog v-if="calculator && $auth.user && $auth.user.role === 'admin'" />

        <v-btn
          v-if="calculator"
          nuxt
          :to="`/admin/ofertas_comparador/prioridad_de_ofertas?comparador=${calculator}`"
          color="green"
        >
          Prioridad de ofertas
        </v-btn>

        <v-btn nuxt :to="`/admin/ofertas_comparador/comercializadoras?comparador=${calculator}`" color="warning">
          Comercializadoras
        </v-btn>

        <v-btn nuxt :to="`/admin/ofertas_comparador/update?comparador=${calculator}`" color="success">
          <v-icon>mdi-plus-box-multiple</v-icon>
        </v-btn>

        <v-btn nuxt :to="`/admin/ofertas_comparador/nuevo_oferta?comparador=${calculator}`" color="success">
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>

    <v-card-text>
      <vue-good-table
        mode="remote"
        fixed-headers
        line-numbers
        :compact-mode="$vuetify.breakpoint.mobile"
        :theme="$vuetify.theme['isDark'] ? 'nocturnal' : 'black-rhino'"
        :row-style-class="rowStyleClassFn"
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
        @on-sort-change="onSortChange"
        @on-per-page-change="onPerPageChange"
        @on-search="onSearch"
        @on-cell-click="onCellClick"
        @on-selected-rows-change="
          selectedRows = $event.selectedRows
          actionsSnackbar = selectedRows.length > 0
        "
      >
        <template slot="column-filter" slot-scope="{ column }">
          <v-checkbox
            v-if="column.filterOptions.isBoolean"
            :value="JSON.parse($route.query[column.field] || 'null')"
            :indeterminate="!['true', 'false'].includes($route.query[column.field])"
            @change="updateBooleanParam(column.field)"
          />
          <v-select
            v-else-if="isSelect(column)"
            :items="column.filterOptions.filterDropdownItems"
            :value="$route.query[column.field]"
            multiple
            clearable
            @input="updateParams2(`${column.field}__in`, ($event || []).join(','))"
          />
          <v-text-field
            v-else-if="column.filterOptions.enabled"
            clearable
            :value="$route.query[column.field]"
            @input="updateParams2(column.field, $event)"
          />
        </template>

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
// import DeleteButton from '@/components/buttons/deleteButton'
import CloseButton from '@/components/buttons/closeButton'
import constants from '@/lib/constants'
export default {
  name: 'AdminOffers',
  components: {
    CloseButton,
    // DeleteButton,
    OfferRequiredFields,
    CalculatorSettingsDialog: () => import('@/components/dialogs/CalculatorSettingsDialog'),
  },
  props: {
    calculator: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    const q = this.$route.query
    return {
      actionsSnackbar: false,
      deleteRowsDialog: false,
      selectedRows: [],
      newName: '',
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
            isBoolean: true,
          },
        },
        {
          label: 'Comparador',
          field: 'calculator',
          formatFn: this.booleanFormat,
          filterOptions: {
            enabled: false,
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
          filterOptions: { enabled: true },
        },
        { label: 'Descripcion', field: 'description', sortable: false, filterOptions: {} },
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
    }),
  },
  async mounted() {
    if (!this.companies.length) await this.$store.dispatch('fetchCompanies')
    await this.refresh()
    this.columns = this.columns.map((column) => {
      if (column.field === 'company') {
        column.filterOptions.filterDropdownItems = this.companies
      } else if (column.field === 'tarif') {
        column.filterOptions.filterDropdownItems = constants.tarifs.concat(constants.tarifsGas)
      }
      return column
    })
  },
  methods: {
    updateBooleanParam(name) {
      const oldRawValue = this.$route.query[name]
      const oldValue = oldRawValue === 'true' ? true : oldRawValue === 'false' ? false : undefined
      let newValue

      switch (oldValue) {
        case true:
          newValue = undefined
          break
        case false:
          newValue = true
          break
        default:
          newValue = false
          break
      }
      this.updateParams2(name, newValue)
    },
    isSelect(column) {
      return (
        column.filterOptions &&
        column.filterOptions.enabled &&
        column.filterOptions.filterDropdownItems &&
        column.filterOptions.filterDropdownItems.length
      )
    },
    rowStyleClassFn(row) {
      return row.active ? '' : 'red'
    },
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
    updateParams2(f, v) {
      this.updateParams({ [f]: v })
    },
    updateParams(newProps) {
      if (this.loading) return
      this.loading = true
      const query = Object.entries(Object.assign({}, this.query, newProps)).reduce(
        (a, [k, v]) => (v || v === false ? ((a[k] = v), a) : a),
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
    async refresh() {
      const fullPath = this.$route.fullPath
      let getParamsString = fullPath.includes('?') ? fullPath.split('?')[1] : 'page=1&itemsPerPage=10'
      if (this.calculator) getParamsString = getParamsString + '&calculator=true'
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
      if (!values) return
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
