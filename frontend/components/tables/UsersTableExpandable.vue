<template>
  <v-data-table
    show-expand
    single-expand
    :expanded.sync="expanded"
    :loading="loading"
    :headers="activeHeaders"
    :items="users"
    :options.sync="query"
    :server-items-length="total"
    :footer-props="{
      itemsPerPageOptions: [10, 50, 100],
      showFirstLastPage: true,
      firstIcon: 'mdi-arrow-collapse-left',
      lastIcon: 'mdi-arrow-collapse-right',
      prevIcon: 'mdi-minus',
      nextIcon: 'mdi-plus',
      itemsPerPageText: `Suma solicitud: ${suma}. Filas por página:`,
    }"
    class="elevation-1"
    @update:options="fetchUsers"
  >
    <template v-slot:top>
      <div class="pa-3">
        <v-row align="center" class="elevation-1 pa-3 flex-wrap" justify="space-around">
          <v-col :cols="showFilters ? 8 : !isSupport ? 11 : 12">
            <v-text-field
              v-model="search"
              :disabled="loading"
              append-icon="mdi-database-search"
              label="Buscar"
              hint="Buscar por id, cups, CIF/DNI, número de teléfono o correo electrónico"
              persistent-hint
              single-line
              @click:append="updateQuery({ search: search })"
              @keydown.enter="updateQuery({ search: search })"
            />
          </v-col>

          <v-col v-if="showFilters" :cols="flexs.cols" :xl="flexs.xl" :lg="flexs.lg" :md="flexs.md" :xs="flexs.xs">
            <v-overflow-btn
              v-model="role"
              :disabled="loading"
              :items="userRoles"
              hint="los clientes son los que firmaron un contrato con nosotros"
              persistent-hint
              class="text-center pa-3"
              label="Tipo de usuario"
              @change="updateQuery({ role: role })"
            >
              <template v-slot:append>
                <add-new-employee @added="fetchUsers" />
              </template>
            </v-overflow-btn>
          </v-col>

          <v-col
            v-if="headers.some((h) => h.includes('responsible'))"
            :cols="flexs.cols"
            :xl="flexs.xl"
            :lg="flexs.lg"
            :md="flexs.md"
            :xs="flexs.xs"
          >
            <v-autocomplete
              :value="query.responsible__in ? query.responsible__in.split(',').map((i) => parseInt(i)) : null"
              label="Responsable"
              :items="responsibles"
              multiple
              item-text="fullname"
              item-value="id"
              clearable
              @change="updateQuery({ responsible__in: $event && $event.length ? $event.join() : null })"
            />
          </v-col>

          <v-col
            v-if="headers.some((h) => h === 'created_at')"
            :cols="flexs.cols"
            :xl="flexs.xl"
            :lg="flexs.lg"
            :md="flexs.md"
            :xs="flexs.xs"
          >
            <date-time-filter
              :value="query.created_at__range"
              label="Fecha de registro"
              range
              @input="
                $event && $event.end
                  ? updateQuery({ created_at__range: `${$event.start},${$event.end}` })
                  : updateQuery({ created_at__range: null })
              "
            />
          </v-col>

          <v-col
            v-if="headers.some((h) => h.includes('fecha_registro'))"
            :cols="flexs.cols"
            :xl="flexs.xl"
            :lg="flexs.lg"
            :md="flexs.md"
            :xs="flexs.xs"
          >
            <date-time-filter
              label="Fecha de registro solicitud"
              range
              :value="query.bids__created_at__range"
              @input="
                $event && $event.end
                  ? updateQuery({ bids__created_at__range: `${$event.start},${$event.end}` })
                  : updateQuery({ bids__created_at__range: null })
              "
            />
          </v-col>

          <v-col
            v-if="headers.some((h) => h === 'fecha_firma')"
            :cols="flexs.cols"
            :xl="flexs.xl"
            :lg="flexs.lg"
            :md="flexs.md"
            :xs="flexs.xs"
          >
            <date-time-filter
              :value="query.bids__fecha_firma__range"
              label="Fecha de firma"
              range
              @input="
                $event && $event.end
                  ? updateQuery({ bids__fecha_firma__range: `${$event.start},${$event.end}` })
                  : updateQuery({ bids__fecha_firma__range: null })
              "
            />
          </v-col>

          <v-col
            v-if="statuses.length > 1"
            :cols="flexs.cols"
            :xl="flexs.xl"
            :lg="flexs.lg"
            :md="flexs.md"
            :xs="flexs.xs"
          >
            <v-select
              v-model="query.statuses_in"
              label="State"
              :items="statuses"
              multiple
              chips
              deletable-chips
              small-chips
              clearable
              @change="updateQuery({ statuses_in: $event })"
            />
          </v-col>

          <template v-if="headers.some((h) => h === 'internal_status') && isSupport">
            <v-col
              v-for="q in [
                { text: 'Doc', value: 'bids__doc' },
                { text: 'Scoring', value: 'bids__scoring' },
                { text: 'Llamada', value: 'bids__call' },
                { text: 'Estado de oferta', value: 'bids__offer_status' },
              ]"
              :key="q.value"
            >
              <v-select
                v-model="query[q.value]"
                :label="q.text"
                clearable
                :items="q.value === 'bids__offer_status' ? offerStatusItems : booleanItems"
                @change="
                  query[q.value] === 'None'
                    ? updateQuery({ [`${q.value}__isnull`]: 'true', [q.value]: null })
                    : updateQuery({ [`${q.value}__isnull`]: null, [q.value]: query[q.value] })
                "
              />
            </v-col>
          </template>
        </v-row>
      </div>
    </template>

    <template v-slot:item.data-table-expand="{ item, isExpanded }">
      <v-btn v-if="item['bids_count']" icon @click="onExpand(item, !isExpanded)">
        <v-icon>mdi-{{ isExpanded ? 'chevron-up' : 'chevron-down' }}</v-icon>
      </v-btn>
    </template>

    <template v-slot:expanded-item="{ item }">
      <td :colspan="headers.length">
        <v-list>
          <v-list-item v-for="bid in bids" :key="bid.id" :to="`${mode}/${item.id}/?bid_id=${bid.id}`">
            <bid-detail :mode="mode" :bid="bid" />
          </v-list-item>
        </v-list>
      </td>
    </template>

    <template v-slot:[`item.fullname`]="{ item }">
      <v-row align="center">
        <v-col>
          <nuxt-link :to="getDetailUrl(item.id)">
            {{ item.fullname }}
          </nuxt-link>
        </v-col>

        <v-col>
          <v-btn icon x-small link :to="getDetailUrl(item.id)" target="_blank">
            <v-icon>mdi-open-in-new</v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </template>
  </v-data-table>
</template>

<script>
import constants from '@/lib/constants'
import { mapState } from 'vuex'
export default {
  name: 'UsersTableExpandable',
  components: {
    BidDetail: () => import('@/components/BidDetail'),
    AddNewEmployee: () => import('@/components/forms/AddNewEmployee'),
    DateTimeFilter: () => import('~/components/DateTimeFilter'),
  },
  props: {
    mode: {
      type: String,
      default: null,
    },
    statuses: {
      type: Array,
      default: () => [],
    },
    listUrl: {
      type: String,
      default: 'users/users',
    },
    allowDelete: {
      type: Boolean,
      default: false,
    },
    showFilters: {
      type: Boolean,
      default: false,
    },
    isSupport: {
      type: Boolean,
      default: false,
    },
    defaultRole: {
      type: String,
      default: null,
    },
    headers: {
      type: Array,
      default: () => [],
    },
    responsible: {
      type: [String, Number],
      default: 0,
    },
    bidsCountHeader: {
      type: String,
      default: 'Solicitud',
    },
  },
  data() {
    const query = this.$route.query
    return {
      constants,
      bids: [],
      expanded: [],
      booleanItems: [
        {
          text: 'OK',
          value: 'True',
        },
        {
          text: 'KO',
          value: 'False',
        },
        {
          text: '-',
          value: 'None',
        },
      ],
      offerStatusItems: [
        {
          text: 'FIRMADA',
          value: '0',
        },
        {
          text: 'PTE FIRMAR',
          value: '1',
        },
        {
          text: '-',
          value: 'None',
        },
      ],
      flexs: { cols: 12, xl: 3, lg: 3, md: 3, sm: 3, xs: 12 },
      userRoles: Object.values(constants.userRoles),
      role: this.defaultRole,
      users: [],
      suma: 0,
      loading: false,
      total: 0,
      search: query.search || '',
      query: {
        ...query,
        sortBy: this.mode === 'tramitacion' ? ['fecha_registro'] : ['fecha_firma'],
        sortDesc: [false],
        statuses_in: query.statuses_in
          ? query.statuses_in.length
            ? query.statuses_in.split(',')
            : query.statuses_in
          : [],
        mustSort: null,
        multiSort: null,
        bids__call: null,
        bids__doc: null,
        bids__scoring: null,
        responsible: this.responsible ? this.responsible : query.responsible ? parseInt(query.responsible) : null,
        page: query.page ? parseInt(query.page) : 1,
        itemsPerPage: query.itemsPerPage ? parseInt(query.itemsPerPage) : 10,
      },
    }
  },
  computed: {
    ...mapState({ responsibles: (state) => state.responsibles }),
    activeHeaders() {
      const headers = [
        { text: 'ID', value: 'id' },
        { text: 'Fecha de registro', value: 'created_at' },
        { text: 'Fecha de registro solicitud', value: 'fecha_registro' },
        { text: 'Fecha firma', value: 'fecha_firma' },
        { text: 'Nombre/Razon social', value: 'fullname', sortable: false },
        { text: 'Tipo de agente', value: 'agent_type' },
        { text: 'Telefono', value: 'phone' },
        { text: 'Ultimo cambio', value: 'last_modified' },
        { text: 'Responsable', value: 'responsible_fn' },
        { text: 'Canal', value: 'canal_fn' },
        { text: this.bidsCountHeader, value: 'bids_count', sortable: false },
        { text: 'Comisiones agente', value: 'paid_count' },
        { text: 'Comisiones canal', value: 'canal_paid_count' },
        { text: 'Estado', value: 'status' },
        { text: 'State', value: 'internal_status' },
        { text: 'Doc', value: 'docs', sortable: false },
        { text: 'Scoring', value: 'scorings', sortable: false },
        { text: 'Llamadas', value: 'calls', sortable: false },
        { text: 'Estado de oferta', value: 'offer_status', sortable: false },
      ].filter((header) => this.headers.includes(header.value))

      if (this.role && this.role !== 'agent') {
        return headers.filter((h) => h.value !== 'agent_type')
      }
      return headers
    },
  },
  async mounted() {
    if (this.headers.some((header) => header.includes('responsible')) && !this.responsibles.length) {
      await this.$store.dispatch('fetchResponsibles')
    }
    if (this.role) this.query.role = this.role
  },
  methods: {
    async onExpand(item, value) {
      if (!value) {
        this.expanded = []
        return
      }
      this.expanded = [item]
      const fields = this.mode.includes('tramitacion')
        ? 'id,internal_status,fecha_firma,created_at,doc,call,scoring,offer_status,offer_status_accesible,success'
        : 'id,internal_status,fecha_firma,created_at,commission,canal_commission,fecha_de_cobro_prevista,paid,canal_paid'
      this.bids = await this.$axios.$get(`/bids/bids/?user=${item.id}&fields=${fields}`)
    },
    getDetailUrl(userId) {
      return `${this.$route.path}/${userId}`
    },

    // other
    async fetchUsers() {
      try {
        this.loading = true
        if (
          String(this.query.page) !== String(this.$route.query.page) ||
          String(this.query.itemsPerPage) !== String(this.$route.query.itemsPerPage)
        ) {
          await this.$router.replace({
            query: Object.entries(this.query).reduce((a, [k, v]) => (v ? ((a[k] = v), a) : a), {}),
          })
        }
        const query = this.getQuery()
        const queryStr = Object.keys(query)
          .filter((k) => query[k] !== null)
          .map((k) => {
            const value = query[k]
            return value instanceof Array ? `${k}=${value.join()}` : `${k}=${value}`
          })
          .join('&')
        const data = await this.$axios.$get(`${this.listUrl}/?${queryStr}`)
        const { results, count, suma } = data
        this.users = results
        this.total = count
        this.suma = suma
      } finally {
        this.loading = false
      }
    },
    getQuery() {
      const query = constants.cleanEmpty({
        ...this.query,
        ordering:
          this.query.sortBy instanceof Array
            ? this.query.sortBy.map((sortBy, idx) => (this.query.sortDesc[idx] ? '+' : '-') + sortBy).join()
            : null,
        fields: this.headers.join(),
        role__isnull: this.role === 'null' ? true : null,
      })
      if (this.mode) query.mode = this.mode
      return query
    },
    async updateQuery(options) {
      options = { ...options, page: 1 }
      Object.keys(options).forEach((key) => {
        const value = options[key]
        if (value) {
          this.query[key] = options[key]
        } else {
          delete this.query[key]
        }
      })
      const q = Object.entries(this.query).filter((entry) => {
        const value = entry[1]
        if (value instanceof Array) return value.length
        return !!value
      })
      if (JSON.stringify(q) !== JSON.stringify(this.query)) await this.$router.replace({ query: q })
      await this.fetchUsers()
    },
  },
}
</script>
