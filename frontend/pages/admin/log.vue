<template>
  <v-card>
    <v-toolbar>
      <v-toolbar-title>Logs</v-toolbar-title>

      <v-spacer />

      <v-toolbar-items>
        <v-btn color="success" :disabled="loading" @click="refresh">
          <v-icon>mdi-refresh</v-icon>
        </v-btn>
      </v-toolbar-items>
    </v-toolbar>

    <v-card-text>
      <v-data-table
        :loading="loading"
        :items="items"
        :headers="headers"
        :options.sync="options"
        :server-items-length="total"
        :footer-props="{
          itemsPerPageOptions: [10, 50, 100, 1000],
          showFirstLastPage: true,
          firstIcon: 'mdi-arrow-collapse-left',
          lastIcon: 'mdi-arrow-collapse-right',
          prevIcon: 'mdi-minus',
          nextIcon: 'mdi-plus',
        }"
        @update:options="refresh"
      >
        <template v-slot:top>
          <v-row>
            <v-col>
              <v-text-field v-model="search" label="Buscar" />
            </v-col>
            <v-col>
              <v-autocomplete
                v-model="filters.user__in"
                :items="users"
                multiple
                item-value="id"
                item-text="fullname"
                label="Usuario"
                clearable
                @change="refresh"
              />
            </v-col>
            <v-col>
              <v-select
                v-model="filters.method__in"
                label="Methods"
                :items="['GET', 'POST', 'PATCH', 'DELETE']"
                multiple
                @change="refresh"
              >
                <template v-slot:item="{ item }">
                  {{ item }}
                  <v-icon :color="formatMethod('', item).color">{{ formatMethod('', item).icon }}</v-icon>
                </template>
              </v-select>
            </v-col>
          </v-row>
        </template>

        <template v-slot:item.requested_at="{ item }">
          {{ formatDt(item.requested_at) }}
        </template>

        <template v-slot:item.method="{ item }">
          <v-icon :color="formatMethod(item.path, item.method).color">
            {{ formatMethod(item.path, item.method).icon }}
          </v-icon>
        </template>

        <template v-slot:item.response="{ item }">
          <v-dialog v-if="item.response" max-width="1000px">
            <template v-slot:activator="{ on }">
              <v-btn icon v-on="on">
                <v-icon>mdi-eye</v-icon>
              </v-btn>
            </template>
            <v-card>
              <v-card-text>
                <pre>{{ item.response }}</pre>
              </v-card-text>
            </v-card>
          </v-dialog>
        </template>

        <template v-slot:item.errors="{ item }">
          <v-dialog v-if="item.errors" max-width="1000px">
            <v-btn icon v-on="on">
              <v-icon>mdi-eye</v-icon>
            </v-btn>
            <v-card>
              <v-card-text>
                <pre>{{ item.errors }}</pre>
              </v-card-text>
            </v-card>
          </v-dialog>
        </template>

        <template v-slot:item.data="{ item }">
          <v-dialog v-if="item.data" max-width="1000px">
            <template v-slot:activator="{ on }">
              <v-btn icon v-on="on">
                <v-icon>mdi-eye</v-icon>
              </v-btn>
            </template>
            <v-card>
              <v-card-text>
                <pre>{{ item.data }}</pre>
              </v-card-text>
            </v-card>
          </v-dialog>
        </template>

        <template v-slot:item.query_params="{ item }">
          <v-dialog v-if="item.query_params && item.query_params !== item.data" max-width="1000px">
            <template v-slot:activator="{ on }">
              <v-btn icon v-on="on">
                <v-icon>mdi-eye</v-icon>
              </v-btn>
            </template>
            <v-card>
              <v-card-text>
                <pre>{{ item.query_params }}</pre>
              </v-card-text>
            </v-card>
          </v-dialog>
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
import { format, parseISO } from 'date-fns'
export default {
  data() {
    return {
      debounceSearchTimeout: null,
      debounceSearch: '',
      users: [],
      filters: {
        user__in: [],
        method__in: ['POST', 'PATCH', 'DELETE'],
      },
      loading: false,
      items: [],
      options: {
        page: 1,
        itemsPerPage: 10,
        sortBy: ['requested_at'],
        sortDesc: [true],
      },
      total: 0,
      headers: [
        {
          text: 'Fecha',
          value: 'requested_at',
        },
        {
          text: 'Usuario',
          value: 'user',
        },
        {
          text: 'Path',
          value: 'path',
        },
        {
          text: 'Method',
          value: 'method',
        },
        {
          text: 'Data',
          value: 'data',
        },
        {
          text: 'Query',
          value: 'query_params',
        },
        {
          text: 'Errors',
          value: 'errors',
        },
      ],
    }
  },
  computed: {
    search: {
      get() {
        return this.debounceSearch
      },
      set(val) {
        if (this.debounceSearchTimeout) clearTimeout(this.debounceSearchTimeout)
        this.debounceSearchTimeout = setTimeout(() => {
          this.debounceSearch = val
        }, 300)
      },
    },
  },
  watch: {
    async debounceSearch() {
      await this.refresh()
    },
  },
  async mounted() {
    await this.refresh()
    await this.fetchUsers()
  },
  methods: {
    async fetchUsers() {
      this.users = await this.$axios.$get('users/users/?fields=id,fullname&role__in=admin,agent,support')
    },
    async refresh() {
      this.loading = true
      const data = await this.$axios.$get(`logs/logs/?${this.query()}`)
      this.total = data.count
      this.items = data.results
      this.loading = false
    },
    query() {
      const opts = this.options
      const ordering = opts.sortBy.length ? (opts.sortDesc[0] ? '-' : '') + opts.sortBy[0] : '-requested_at'
      const filters = Object.keys(this.filters)
        .filter((k) => {
          const val = this.filters[k]
          return val instanceof Array ? !!val.length : true
        })
        .map((k) => k + '=' + this.filters[k])
        .join('&')
      const params = [
        'fields=' +
          this.headers
            .map((h) => h.value)
            .filter((h) => h)
            .join(','),
        'page=' + opts.page,
        'size=' + opts.itemsPerPage || 10,
        'ordering=' + ordering,
        'search=' + this.search,
        filters,
      ]
      return params.join('&')
    },
    formatDt(dt) {
      return format(parseISO(dt), 'dd/MM/yyyy HH:mm')
    },
    formatMethod(aep, method) {
      let icon
      let color
      method = method.toLowerCase()
      if (method === 'get') {
        icon = 'mdi-book'
        color = 'info'
      } else if (method === 'post') {
        if (aep.indexOf('api/calculator/calculate') !== -1) {
          icon = 'mdi-calculator'
        } else {
          icon = 'mdi-cloud-upload'
        }
        color = 'success'
      } else if (method === 'patch') {
        icon = 'mdi-pencil'
        color = 'warning'
      } else if (method === 'delete') {
        icon = 'mdi-trash-can-outline'
        color = 'error'
      }
      return { icon, color }
    },
  },
}
</script>
