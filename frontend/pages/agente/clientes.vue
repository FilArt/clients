<template>
  <v-card>
    <v-card-text>
      <agent-header />
    </v-card-text>

    <v-card-text>
      <users-table :client-role="clientRole" :additional-headers="additionalHeaders" />
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
      clientRole: constants.clientRoles.clients.value,
      additionalHeaders: [
        {
          index: 3,
          value: {
            text: 'Responsable',
            value: 'responsible',
          },
        },
        {
          index: 4,
          value: {
            text: 'Origin',
            value: 'affiliate',
          },
        },
      ],
    }
  },
}
</script>
