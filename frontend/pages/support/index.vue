<template>
  <v-card>
    <v-card-text v-if="$auth.user.role === 'admin'">
      <admin-header />
    </v-card-text>

    <v-card-text>
      <v-data-table :headers="headers" :items="items">
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
}
</script>
