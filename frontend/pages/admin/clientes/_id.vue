<template>
  <v-card class="pa-3">
    <v-card-title>{{ user.fullname }}</v-card-title>

    <v-card-text>
      <user-detail-data
        :user-id="user.id"
        @user-updated="
          user = null
          user = $event
        "
      />
    </v-card-text>

    <v-card-text>
      <v-tabs v-model="tabs" centered>
        <v-tab :disabled="!bids.length">Solicitud ({{ bids.length }})</v-tab>
        <v-tab :disabled="!calls.length"> Llamadas ({{ calls.length }}) </v-tab>
        <v-tab :disabled="!history.length">Historia ({{ history.length }})</v-tab>
        <v-tab :disabled="!puntos.length"> Puntos suministros ({{ puntos.length }}) </v-tab>

        <v-tabs-items v-model="tabs">
          <v-tab-item>
            <v-list three-line subheader nav shaped>
              <v-subheader inset> Solicitudes </v-subheader>

              <v-list-item v-for="bid in bids" :key="bid.id" nuxt :to="`/bids/${bid.id}`">
                <v-list-item-content>
                  <v-list-item-title v-text="bid.offer_name" />
                  <v-list-item-subtitle v-text="'id: ' + bid.id" />
                  <v-list-item-subtitle v-text="bid.created_at" />
                </v-list-item-content>

                <v-list-item-content>
                  {{ bid.status }}
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-tab-item>

          <v-tab-item>
            <v-list>
              <v-list-item v-for="call in calls" :key="call.id">
                <v-list-item-content>
                  <audio :src="call" type="audio/mp3" controls></audio>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-tab-item>

          <v-tab-item v-if="history.length">
            <history-list :history="history" />
          </v-tab-item>

          <v-tab-item>
            <puntos-list :puntos="puntos" @punto-updated="fetchPuntos" />
          </v-tab-item>
        </v-tabs-items>
      </v-tabs>
    </v-card-text>

    <chat v-if="participant" :participant="participant" />
  </v-card>
</template>

<script>
export default {
  components: {
    Chat: () => import('~/components/chat/Chat'),
    PuntosList: () => import('~/components/puntos/PuntosList'),
    HistoryList: () => import('~/components/history/HistoryList'),
    UserDetailData: () => import('@/components/forms/UserDetailData'),
  },
  async asyncData({ params, $axios }) {
    const user = await $axios.$get(`/users/users/${params.id}/?fields=phone,phones,email,avatar,bids`)

    const phoneNumbers = [user.phone, ...user.phones.map((phone) => phone.number)].filter((p) => p)
    let calls = []
    if (phoneNumbers.length) {
      calls = await $axios.$get(`users/calls/${user.id}`)
    }

    const participant = {
      id: params.id,
      name: user.email,
      imageUrl: user.avatar || '',
    }
    return {
      user,
      participant,
      calls,
      bids: user.bids,
      puntos: await $axios.$get(`/users/puntos/?user=${params.id}`),
      history: await $axios.$get(`/bids/history/?user=${params.id}`),
    }
  },
  computed: {
    tabs() {
      return this.bids.length ? 0 : null
    },
  },
  methods: {
    async fetchPuntos() {
      this.puntos = await this.$axios.$get(`/users/puntos/?user=${this.user.id}`)
    },
  },
}
</script>
