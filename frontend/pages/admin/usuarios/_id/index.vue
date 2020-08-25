<template>
  <v-card class="pa-3">
    <v-card-text>
      <admin-header />
    </v-card-text>

    <v-card-title>{{ fullname }}</v-card-title>

    <v-card-text>
      <v-row class="flex-wrap">
        <v-col md="6" cols="12">
          <v-toolbar elevation="10" short dense>
            <v-spacer />
            <v-toolbar-title>
              Datos de contacto
            </v-toolbar-title>
            <v-spacer />
          </v-toolbar>
          <v-card elevation="10" class="pa-3">
            <v-row>
              <v-col v-for="item in contactInfo" :key="item.value" xl="4" md="6" cols="12">
                <v-text-field :prepend-icon="item.icon" :label="item.text" :value="item.value" filled />
              </v-col>
            </v-row>
          </v-card>
        </v-col>

        <v-col>
          <v-toolbar short dense elevation="10">
            <v-spacer />
            <v-toolbar-title>
              Otro
            </v-toolbar-title>
            <v-spacer />
          </v-toolbar>
          <v-card elevation="10" class="pa-3">
            <v-row class="flex-wrap">
              <v-col v-for="date in datesInfo" :key="date.value" xl="4" md="6" cols="12">
                <v-text-field :prepend-icon="date.icon" :label="date.text" :value="date.value" outlined shaped />
              </v-col>
            </v-row>
          </v-card>
        </v-col>
      </v-row>
    </v-card-text>

    <v-card-text>
      <v-tabs v-model="tabs" centered>
        <v-tab>Solicitud ({{ user.bids.length }})</v-tab>
        <v-tab :disabled="!calls.length"> Llamadas ({{ calls.length }}) </v-tab>
        <v-tab>Historia</v-tab>
        <v-tab :disabled="!puntos.length"> Puntos suministros ({{ puntos.length }}) </v-tab>

        <v-tabs-items v-model="tabs">
          <v-tab-item>
            <v-list three-line subheader nav shaped>
              <v-subheader inset>
                Solicitudes
              </v-subheader>

              <v-list-item v-for="bid in user.bids" :key="bid.id" nuxt :to="`/bids/${bid.id}`">
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
                  {{ call.called_at }}
                  <audio :src="call.file" type="audio/mp3" controls></audio>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-tab-item>

          <v-tab-item v-if="history.length">
            <history-list :history="history" />
          </v-tab-item>

          <v-tab-item>
            <puntos-list :puntos="puntos" editable @punto-updated="fetchPuntos" />
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
    AdminHeader: () => import('~/components/admin/AdminHeader'),
    Chat: () => import('~/components/chat/Chat'),
    PuntosList: () => import('~/components/puntos/PuntosList'),
    HistoryList: () => import('~/components/history/HistoryList'),
  },
  async asyncData({ params, $axios }) {
    const user = await $axios.$get(`/users/users/${params.id}/`)

    const phoneNumbers = [user.phone, ...user.phones.map((phone) => phone.number)].filter((p) => p)
    let calls = []
    if (phoneNumbers.length) {
      calls = await $axios.$get(`users/calls/?phone_numbers=${phoneNumbers}`)
    }

    const participant = {
      id: user.id,
      name: user.email,
      imageUrl: user.avatar || '',
    }
    return {
      user,
      participant,
      calls,
      puntos: await $axios.$get(`/users/puntos/?user=${params.id}`),
      history: await $axios.$get(`/bids/history/?user=${params.id}`),
      contactInfo: [
        {
          icon: 'mdi-account',
          text: 'Representante legal',
          value: user.legal_representative,
        },
        ...[...user.phones, { number: user.phone }]
          .filter((n) => n)
          .map((phone) => {
            return {
              icon: 'mdi-phone',
              text: 'Telefono',
              value: phone.number,
            }
          }),
        {
          icon: 'mdi-email',
          text: 'Email',
          value: user.email,
        },
      ],
      datesInfo: [
        {
          icon: 'mdi-calendar',
          text: 'Ultima entrada',
          value: user.last_login,
        },
        {
          icon: 'mdi-calendar',
          text: 'Fecha de registro',
          value: user.date_joined,
        },
        {
          icon: 'mdi-calendar',
          text: 'Fecha firma',
          value: user.last_modified,
        },
        {
          icon: 'mdi-account',
          text: 'Responsable',
          value: user.responsible,
        },
        {
          icon: 'mdi-target',
          text: 'Origin',
          value: user.affiliate,
        },
      ],
    }
  },
  data() {
    return {
      tabs: 0,
    }
  },
  computed: {
    fullname() {
      const u = this.user
      let fullname = [u.first_name, u.last_name]
        .filter((name) => !!name)
        .join(' ')
        .trim()
      return fullname && fullname.length ? fullname : u.email
    },
  },
  methods: {
    async fetchPuntos() {
      this.puntos = await this.$axios.$get(`/users/puntos/?user=${this.user.id}`)
    },
  },
}
</script>
