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

    <v-card-title>Solicitudes</v-card-title>

    <v-card-text>
      <v-data-table
        :headers="[
          {
            text: 'ID',
            value: 'id',
          },
          {
            text: 'Estado',
            value: 'status',
          },
          {
            text: 'Fecha firma',
            value: 'fecha_firma',
          },
          {
            text: 'Commissiones',
            value: 'mymoney',
          },
          {
            text: 'Fecha de cobro prevista',
            value: 'fecha_de_cobro_prevista',
          },
        ]"
        :items="user.bids"
      />
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  components: {
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
