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

    <template v-slot:[`item.company`]="{ item }">
      {{ item.company.name }}
    </template>

    <template v-slot:[`item.name`]="{ item }">
      <v-edit-dialog :return-value.sync="item.name" @save="save(item.id, { name: item.name })">
        <div class="truncate">
          {{ item.name }}
        </div>
        <template v-slot:input>
          <v-text-field v-model="item.name" label="Editar" single-line counter></v-text-field>
        </template>
      </v-edit-dialog>
    </template>

    <template v-slot:[`item.description`]="{ item }">
      <v-edit-dialog :return-value.sync="item.description" @save="save(item.id, { description: item.description })">
        <div class="truncate">
          {{ item.description }}
        </div>
        <template v-slot:input>
          <v-text-field v-model="item.description" label="Editar" single-line counter></v-text-field>
        </template>
      </v-edit-dialog>
    </template>

    <template v-slot:[`item.p1`]="{ item }">
      <v-edit-dialog :return-value.sync="item.p1" @save="save(item.id, { p1: item.p1 })">
        <div class="truncate">
          {{ item.p1 }}
        </div>
        <template v-slot:input>
          <v-text-field v-model="item.p1" label="Editar" single-line counter></v-text-field>
        </template>
      </v-edit-dialog>
    </template>

    <template v-slot:[`item.p2`]="{ item }">
      <v-edit-dialog :return-value.sync="item.p2" @save="save(item.id, { p2: item.p2 })">
        <div class="truncate">
          {{ item.p2 }}
        </div>
        <template v-slot:input>
          <v-text-field v-model="item.p2" label="Editar" single-line counter></v-text-field>
        </template>
      </v-edit-dialog>
    </template>

    <template v-slot:[`item.p3`]="{ item }">
      <v-edit-dialog :return-value.sync="item.p3" @save="save(item.id, { p3: item.p3 })">
        <div class="truncate">
          {{ item.p3 }}
        </div>
        <template v-slot:input>
          <v-text-field v-model="item.p3" label="Editar" single-line counter></v-text-field>
        </template>
      </v-edit-dialog>
    </template>

    <template v-slot:[`item.c1`]="{ item }">
      <v-edit-dialog :return-value.sync="item.c1" @save="save(item.id, { c1: item.c1 })">
        <div class="truncate">
          {{ item.c1 }}
        </div>
        <template v-slot:input>
          <v-text-field v-model="item.c1" label="Editar" single-line counter></v-text-field>
        </template>
      </v-edit-dialog>
    </template>

    <template v-slot:[`item.c2`]="{ item }">
      <v-edit-dialog :return-value.sync="item.c2" @save="save(item.id, { c2: item.c2 })">
        <div class="truncate">
          {{ item.c2 }}
        </div>
        <template v-slot:input>
          <v-text-field v-model="item.c2" label="Editar" single-line counter></v-text-field>
        </template>
      </v-edit-dialog>
    </template>

    <template v-slot:[`item.c3`]="{ item }">
      <v-edit-dialog :return-value.sync="item.c3" @save="save(item.id, { c3: item.c3 })">
        <div class="truncate">
          {{ item.c3 }}
        </div>
        <template v-slot:input>
          <v-text-field v-model="item.c3" label="Editar" single-line counter></v-text-field>
        </template>
      </v-edit-dialog>
    </template>

    <template v-slot:[`item.tarif`]="{ item }">
      <v-edit-dialog :return-value.sync="item.tarif" @save="save(item.id, { tarif: item.tarif })">
        <div class="truncate">
          {{ item.tarif }}
        </div>
        <template v-slot:input>
          <v-text-field v-model="item.tarif" label="Editar" single-line counter></v-text-field>
        </template>
      </v-edit-dialog>
    </template>

    <template v-slot:[`item.agent_commissions`]="{ item }">
      <v-edit-dialog
        :return-value.sync="item.agent_commissions"
        @save="save(item.id, { agent_commissions: item.agent_commissions })"
      >
        <div class="truncate">
          {{ item.agent_commissions }}
        </div>
        <template v-slot:input>
          <v-text-field v-model="item.agent_commissions" label="Editar" single-line counter></v-text-field>
        </template>
      </v-edit-dialog>
    </template>

    <template v-slot:[`item.cannal_commissions`]="{ item }">
      <v-edit-dialog
        :return-value.sync="item.cannal_commissions"
        @save="save(item.id, { cannal_commissions: item.cannal_commissions })"
      >
        <div class="truncate">
          {{ item.cannal_commissions }}
        </div>
        <template v-slot:input>
          <v-text-field v-model="item.cannal_commissions" label="Editar" single-line counter></v-text-field>
        </template>
      </v-edit-dialog>
    </template>

    <template v-slot:[`item.is_price_permanent`]="{ item }">
      <v-edit-dialog
        :return-value.sync="item.is_price_permanent"
        @save="save(item.id, { is_price_permanent: item.is_price_permanent })"
      >
        <div class="truncate">
          {{ item.is_price_permanent }}
        </div>
        <template v-slot:input>
          <v-text-field v-model="item.is_price_permanent" label="Editar" single-line counter></v-text-field>
        </template>
      </v-edit-dialog>
    </template>

    <template v-slot:[`item.power_min`]="{ item }">
      <v-edit-dialog :return-value.sync="item.power_min" @save="save(item.id, { power_min: item.power_min })">
        <div class="truncate">
          {{ item.power_min }}
        </div>
        <template v-slot:input>
          <v-text-field v-model="item.power_min" label="Editar" single-line counter></v-text-field>
        </template>
      </v-edit-dialog>
    </template>

    <template v-slot:[`item.power_max`]="{ item }">
      <v-edit-dialog :return-value.sync="item.power_max" @save="save(item.id, { power_max: item.power_max })">
        <div class="truncate">
          {{ item.power_max }}
        </div>
        <template v-slot:input>
          <v-text-field v-model="item.power_max" label="Editar" single-line counter></v-text-field>
        </template>
      </v-edit-dialog>
    </template>

    <template v-slot:[`item.consumption_max`]="{ item }">
      <v-edit-dialog
        :return-value.sync="item.consumption_max"
        @save="save(item.id, { consumption_max: item.consumption_max })"
      >
        <div class="truncate">
          {{ item.consumption_max }}
        </div>
        <template v-slot:input>
          <v-text-field v-model="item.consumption_max" label="Editar" single-line counter></v-text-field>
        </template>
      </v-edit-dialog>
    </template>

    <template v-slot:[`item.consumption_min`]="{ item }">
      <v-edit-dialog
        :return-value.sync="item.consumption_min"
        @save="save(item.id, { consumption_min: item.consumption_min })"
      >
        <div class="truncate">
          {{ item.consumption_min }}
        </div>
        <template v-slot:input>
          <v-text-field v-model="item.consumption_min" label="Editar" single-line counter></v-text-field>
        </template>
      </v-edit-dialog>
    </template>

    <template v-slot:[`item.client_type`]="{ item }">
      <v-edit-dialog :return-value.sync="item.client_type" @save="save(item.id, { client_type: item.client_type })">
        <div class="truncate">
          {{ item.client_type }}
        </div>
        <template v-slot:input>
          <v-text-field v-model="item.client_type" label="Editar" single-line counter></v-text-field>
        </template>
      </v-edit-dialog>
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
  max-width: 200px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
