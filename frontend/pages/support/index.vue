<template>
  <v-card>
    <v-card-text v-if="$auth.user.role === 'admin'">
      <admin-header />
    </v-card-text>

    <v-card-text>
      <v-data-table :headers="headers" :items="items" :loading="loading">
        <template v-slot:top>
          <v-row align="center">
            <v-col>
              <v-text-field
                v-model="search"
                append-icon="mdi-magnify"
                label="Buscar (id, CUPS, cliente nombre)"
                single-line
                hide-details
              ></v-text-field>
            </v-col>

            <v-col>
              <status-select v-model="status" all />
            </v-col>
          </v-row>
        </template>

        <template v-slot:item.user="{ item }">
          <td colspan="1">
            <nuxt-link :to="`/support/${item.id}`">
              {{ item.user }}
            </nuxt-link>
          </td>
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  components: {
    AdminHeader: () => import('~/components/admin/AdminHeader'),
    StatusSelect: () => import('~/components/selects/StatusSelect'),
  },
  async asyncData({ $axios }) {
    const items = await $axios.$get('bids/bids/?support=true')
    return {
      items,
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'Usuario', value: 'user' },
        { text: 'Estado', value: 'status' },
        { text: 'Fecha de creación', value: 'created_at' },
      ],
    }
  },
  data() {
    return {
      loading: false,
      search: '',
      status: null,
    }
  },
  watch: {
    async search(val) {
      if (this.loading) return
      this.loading = true
      const aep = 'bids/bids/?support=true'
      this.items = await this.$axios.$get(val ? aep + '&search=' + val : aep)
      this.loading = false
    },
    async status(val) {
      if (this.loading) return
      this.loading = true
      const aep = 'bids/bids/?support=true'
      this.items = await this.$axios.$get(val ? aep + '&status=' + val : aep)
      this.loading = false
    },
  },
}
</script>
