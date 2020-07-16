<template>
  <v-card>
    <v-card-text>
      <v-data-table :headers="headers" :items="items">
        <template v-slot:item.actions="{ item }">
          <td colspan="1">
            <v-btn icon nuxt color="primary" :to="`/support/${item.id}`">
              <v-icon>mdi-play</v-icon>
            </v-btn>
          </td>
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  async asyncData({ $axios }) {
    const items = await $axios.$get('bids/bids/')
    const headers = [
      { text: 'ID', value: 'id' },
      { text: 'Usuario', value: 'user' },
      { text: 'Estado', value: 'status' },
      { text: 'Fecha de creación', value: 'created_at' },
    ].concat({
      text: null,
      value: 'actions',
    })
    return {
      items,
      headers,
    }
  },
}
</script>
