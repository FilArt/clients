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
          itemsPerPageOptions: [10, 50, 100],
          showFirstLastPage: true,
          firstIcon: 'mdi-arrow-collapse-left',
          lastIcon: 'mdi-arrow-collapse-right',
          prevIcon: 'mdi-minus',
          nextIcon: 'mdi-plus',
        }"
        @update:options="refresh"
      >
        <template v-slot:top>
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
        </template>

        <template v-slot:item.requested_at="{ item }">
          {{ formatDt(item.requested_at) }}
        </template>

        <template v-slot:item.response="{ item }">
          <v-dialog>
            <template v-slot:activator="{ on }">
              <v-btn v-on="on">show</v-btn>
            </template>
            <v-card>
              {{ item.response }}
            </v-card>
          </v-dialog>
        </template>

        <template v-slot:item.errors="{ item }">
          <v-dialog>
            <template v-slot:activator="{ on }">
              <v-btn v-on="on">show</v-btn>
            </template>
            <v-card>
              {{ item.errors }}
            </v-card>
          </v-dialog>
        </template>

        <template v-slot:item.data="{ item }">
          <v-dialog>
            <template v-slot:activator="{ on }">
              <v-btn v-on="on">show</v-btn>
            </template>
            <v-card>
              {{ item.data }}
            </v-card>
          </v-dialog>
        </template>

        <template v-slot:item.query_params="{ item }">
          <v-dialog>
            <template v-slot:activator="{ on }">
              <v-btn v-on="on">show</v-btn>
            </template>
            <v-card>
              {{ item.query_params }}
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
      users: [],
      filters: {
        user__in: [],
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
  async mounted() {
    await this.refresh()
    await this.fetchUsers()
  },
  methods: {
    async fetchUsers() {
      this.users = await this.$axios.$get('users/users/?fields=id,fullname')
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
        filters,
      ]
      return params.join('&')
    },
    formatDt(dt) {
      return format(parseISO(dt), 'dd/MM/yyyy HH:mm')
    },
  },
}
</script>
