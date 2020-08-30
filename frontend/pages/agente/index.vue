<template>
  <v-card>
    <v-card-text>
      <agent-header />
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  components: { AgentHeader: () => import('@/components/agent/AgentHeader') },
}
</script>
