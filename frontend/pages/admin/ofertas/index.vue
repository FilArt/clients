<template>
  <v-data-table
    :headers="headers"
    :items="items"
    :options.sync="options"
    :server-items-length="total"
    :loading="loading"
    :footer-props="{
      itemsPerPageOptions: [10, 50, 100, 1000],
      showFirstLastPage: true,
      firstIcon: 'mdi-arrow-collapse-left',
      lastIcon: 'mdi-arrow-collapse-right',
      prevIcon: 'mdi-minus',
      nextIcon: 'mdi-plus',
    }"
    class="elevation-1"
  >
    <template v-slot:top>
      <v-alert color="warning"> Tipo de cliente: 0 - Fisico, 1 - Negocio </v-alert>
    </template>

    <template v-slot:item="{ item }">
      <tr>
        <td v-for="header in headers" :key="header.value">
          <v-edit-dialog
            :return-value-sync="item[header.value]"
            @save="save(item.id, { [header.value]: item[header.value] })"
          >
            <div v-if="header.value === 'company'">
              {{ item[header.value].name }}
            </div>
            <div v-else-if="header.value === 'required_fields'" class="truncate">
              <small v-for="(rf, idx) in item[header.value] || []" :key="idx">{{ rf.text }},</small>
            </div>
            <div v-else class="truncate">
              {{ item[header.value] }}
            </div>
            <template v-slot:input>
              <v-select
                v-if="header.value === 'required_fields'"
                v-model="item[header.value]"
                :items="[
                  { value: 'photo_cif1', text: 'Foto CIF' },
                  { value: 'photo_dni1', text: 'Foto DNI' },
                  { value: 'photo_dni2', text: 'Foto DNI reverso' },
                  { value: 'photo_factura', text: 'Foto factura' },
                  { value: 'photo_factura_1', text: 'Foto factura reverso' },
                  { value: 'photo_recibo1', text: 'Foto Recibo de Autónomo' },
                  { value: 'recibo1', text: 'Recibo de Autónomo' },
                  { value: 'cif', text: 'CIF' },
                  { value: 'dni', text: 'DNI' },
                  { value: 'phone', text: 'Telefono' },
                ]"
                multiple
                @change="save(item.id, { required_fields: item[header.value] })"
              ></v-select>

              <v-text-field v-else v-model="item[header.value]" single-line counter />
            </template>
          </v-edit-dialog>
        </td>
      </tr>
    </template>
  </v-data-table>
</template>

<script>
export default {
  components: {
    // CompanySelect: () => import('~/components/selects/CompanySelect'),
  },
  data() {
    const headers = [
      {
        text: 'ID',
        value: 'id',
      },
      {
        text: 'Comers',
        value: 'company',
      },
      {
        text: 'Nombre',
        value: 'name',
      },
      {
        text: 'Descripcion',
        value: 'description',
      },
      {
        text: 'P1',
        value: 'p1',
      },
      {
        text: 'P2',
        value: 'p2',
      },
      {
        text: 'P3',
        value: 'p3',
      },
      {
        text: 'C1',
        value: 'c1',
      },
      {
        text: 'C2',
        value: 'c2',
      },
      {
        text: 'C3',
        value: 'c3',
      },
      {
        text: 'Tarifa',
        value: 'tarif',
      },
      {
        text: 'Potencia min',
        value: 'power_min',
      },
      {
        text: 'Potencia max',
        value: 'power_max',
      },
      {
        text: 'Consumo min',
        value: 'consumption_min',
      },
      {
        text: 'Consumo max',
        value: 'consumption_max',
      },
      {
        text: 'Tipo de cliente',
        value: 'client_type',
      },
      {
        text: 'Tipo de precio',
        value: 'is_price_permanent',
      },
      {
        text: 'Canal comisiones',
        value: 'canal_commission',
      },
      {
        text: 'Agente comisiones',
        value: 'agent_commission',
      },
      {
        text: 'Campos obligatorio',
        value: 'required_fields',
      },
    ]
    const q = this.$route.query
    return {
      loading: false,
      items: [],
      headers,
      total: 0,
      options: {
        ...q,
        page: q.page ? parseInt(q.page) : 1,
        itemsPerPage: q.itemsPerPage ? parseInt(q.itemsPerPage) : 10,
      },
    }
  },
  watch: {
    options: {
      async handler() {
        try {
          const ordering = this.options.sortDesc[0] ? this.options.sortBy : `-${this.options.sortBy}`
          const query = {
            ...this.options,
            ordering: ordering.length > 3 ? ordering : null,
          }
          await this.$router.replace({
            query: Object.entries(query).reduce((a, [k, v]) => (v ? ((a[k] = v), a) : a), {}),
          })
        } catch (e) {
          console.warn(e)
        }
        await this.refresh()
      },
      deep: true,
    },
  },
  methods: {
    async save(id, data) {
      try {
        await this.$axios.$patch(`calculator/admin_offers/${id}/`, data)
      } catch (e) {
        const err = Object.values(e.response.data)[0].join('; ')
        await this.$swal({ title: 'Error', text: err, icon: 'error' })
      } finally {
        await this.refresh()
      }
    },
    async refresh() {
      this.loading = true
      try {
        const getParamsString = this.$route.fullPath.split('?')[1]
        const data = await this.$axios.$get(`calculator/admin_offers/?${getParamsString}`)
        this.total = data.count
        this.items = data.results
      } catch (e) {
        console.error(e)
      } finally {
        this.loading = false
      }
    },
  },
}
</script>

<style scoped>
.truncate {
  max-width: 100px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
