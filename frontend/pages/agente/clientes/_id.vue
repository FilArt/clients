<template>
  <v-card flat>
    <v-toolbar dense>
      <v-toolbar-title>
        <v-btn icon color="error" @click="$router.back()">
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        {{ user.fullname }}
      </v-toolbar-title>
    </v-toolbar>

    <v-card-text>
      <user-detail-data
        :user-id="$route.params.id"
        @user-updated="
          user = null
          user = $event
        "
      />
    </v-card-text>

    <v-card-text>
      <v-tabs v-model="tabs" centered>
        <v-tab>Solicitudes</v-tab>
        <v-tab :disabled="!puntos.length">Puntos suministros ({{ puntos.length }})</v-tab>

        <v-tabs-items v-model="tabs">
          <v-tab-item>
            <solicitudes-bar :user-id="$route.params.id" />
          </v-tab-item>

          <v-tab-item>
            <puntos-list :puntos="puntos" @punto-updated="fetchPuntos" />
          </v-tab-item>
        </v-tabs-items>
      </v-tabs>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  components: {
    SolicitudesBar: () => import('@/components/support/SolicitudesBar'),
    PuntosList: () => import('~/components/puntos/PuntosList'),
    UserDetailData: () => import('@/components/forms/UserDetailData'),
  },
  async asyncData({ params, $axios }) {
    const user = await $axios.$get(`/users/users/${params.id}/?fields=phone,phone_city,email,avatar`)

    const participant = {
      id: params.id,
      name: user.email,
      imageUrl: user.avatar || '',
    }
    return {
      user,
      participant,
      puntos: await $axios.$get(`/users/puntos/?user=${params.id}`),
      tabs: null,
    }
  },
  methods: {
    async fetchPuntos() {
      this.puntos = await this.$axios.$get(`/users/puntos/?user=${this.user.id}`)
    },
  },
}
</script>
