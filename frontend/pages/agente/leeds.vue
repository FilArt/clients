<template>
  <v-card>
    <v-card-text>
      <agent-header />
    </v-card-text>

    <v-card-text>
      <users-table :client-role="clientRole" />
    </v-card-text>
  </v-card>
</template>

<script>
import constants from '@/lib/constants'

export default {
  components: {
    AgentHeader: () => import('@/components/agent/AgentHeader'),
    UsersTable: () => import('@/components/tables/UsersTable'),
  },
  data() {
    return {
      clientRole: constants.clientRoles.leeds.value,
    }
  },
}
</script>
