<template>
  <v-card>
    <v-card-text>
      <admin-header />
    </v-card-text>

    <v-card-text>
      <users-table :client-role="userRole" allow-delete :additional-headers="additionalHeaders" />
    </v-card-text>
  </v-card>
</template>

<script>
import constants from '@/lib/constants'

export default {
  components: {
    AdminHeader: () => import('@/components/admin/AdminHeader'),
    UsersTable: () => import('@/components/tables/UsersTable'),
  },
  data() {
    return {
      userRole: constants.clientRoles.leeds.value,
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
