<template>
  <v-card>
    <v-card-text>
      <agent-header />
    </v-card-text>

    <v-card-text>
      <v-data-table :headers="headers" :items="items"> </v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  components: { AgentHeader: () => import('@/components/agent/AgentHeader') },
  async asyncData({ $axios }) {
    const items = await $axios.$get('tramitacion/')
    const headers = items.length
      ? Object.keys(items[0]).map((k) => {
          return {
            text: k,
            value: k,
          }
        })
      : []
    return {
      items,
      headers,
    }
  },
}
</script>
