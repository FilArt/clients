<template>
  <v-card>
    <v-card-title>Analytic</v-card-title>
    <v-card-text v-if="agents && agents.length">
      <v-data-table :items="items" :headers="headers" hide-default-footer :items-per-page="9999" :sort-by="['ID']" />
    </v-card-text>
    <v-card-text v-else>
      <v-progress-circular indeterminate />
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'AgentsAnalytics',
  async asyncData({ $axios }) {
    const agents = await $axios.$get('/users/manage_users/analytic_new/')
    return { agents }
  },
  computed: {
    headers() {
      return this.items.length ? Object.keys(this.items[0]).map((x) => ({ text: x, value: x })) : []
    },
    items() {
      return this.agents && this.agents.length ? this.agents : []
    },
  },
}
</script>
