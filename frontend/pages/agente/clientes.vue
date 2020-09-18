<template>
  <v-card>
    <v-card-text>
      <users-table :client-roles="clientRoles" detail-url="/agente" use-full-name />
    </v-card-text>
  </v-card>
</template>

<script>
import constants from '@/lib/constants'

export default {
  components: {
    UsersTable: () => import('@/components/tables/UsersTable'),
  },
  data() {
    return {
      clientRoles: [constants.clientRoles.clients.value],
    }
  },
}
</script>
