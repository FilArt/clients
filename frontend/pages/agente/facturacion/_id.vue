<template>
  <v-card>
    <v-card-text>
      <v-toolbar>
        <v-toolbar-title>
          {{ user.fullname }}
        </v-toolbar-title>
      </v-toolbar>
      <user-detail-data :user-id="$route.params.id" />
    </v-card-text>

    <v-divider />

    <v-card-text>
      <solicitudes-bar :user-id="$route.params.id" />
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  components: {
    SolicitudesBar: () => import('@/components/support/SolicitudesBar'),
    UserDetailData: () => import('@/components/forms/UserDetailData'),
  },
  async asyncData({ $axios, params }) {
    const user = await $axios.$get(`users/users/${params.id}/`)

    return {
      user,
    }
  },
  data() {
    return {
      cols: 3,
    }
  },
  methods: {
    async refresh() {
      this.user = await this.$axios.$get(`users/users/${this.user.id}/`)
    },
  },
}
</script>
