<template>
  <v-card>
    <v-card-text>
      <admin-header />
    </v-card-text>

    <v-card-text>
      <users-table :default-role="userRole" allow-delete />
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
      userRole: constants.userRoles.leeds.value,
    }
  },
}
</script>
