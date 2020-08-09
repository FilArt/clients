<template>
  <v-card>
    <v-card-text>
      <admin-header />
    </v-card-text>

    <v-card-title>{{ fullname }}</v-card-title>

    <v-card-text>
      <v-row>
        <v-col>
          <p>Telefonos</p>
          <p v-for="phone in user.phones" :key="phone.id">
            {{ phone.number }}
          </p>
        </v-col>

        <v-col>
          <p>Email: {{ user.email }}</p>
          <p>DNI: {{ user.dni }}</p>
          <p>DNI/CIF: {{ user.dni_cif }}</p>
          <p>Representante legal: {{ user.legal_representative }}</p>
        </v-col>

        <v-col>
          <p>Fecha de creación: {{ user.date_joined }}</p>
        </v-col>
      </v-row>
    </v-card-text>

    <v-card-text>
      <v-tabs v-model="tabs" centered>
        <v-tab>Bids ({{ user.bids.length }})</v-tab>
        <v-tab :disabled="!calls.length"> Llamadas ({{ calls.length }}) </v-tab>
        <v-tab>Historia</v-tab>
        <v-tab :disabled="!puntos.length"> Puntos suministros ({{ puntos.length }}) </v-tab>
        <v-tab :disabled="!attachments.length"> Documentos ({{ attachments.length }}) </v-tab>

        <v-tabs-items v-model="tabs">
          <v-tab-item>
            <v-list three-line subheader nav shaped>
              <v-subheader inset>
                Bids
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

          <v-tab-item>
            <history-list :history="history" />
          </v-tab-item>

          <v-tab-item>
            <puntos-list :puntos="puntos" editable @punto-updated="fetchPuntos" />
          </v-tab-item>

          <v-tab-item>
            <v-row v-for="attachment in attachments" :key="attachment.id">
              <v-col>
                <v-chip target="_blank" :href="attachment.attachment">
                  {{ attachment.type_verbose_name }} (punto: {{ attachment.punto }})
                </v-chip>
              </v-col>
            </v-row>
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
      puntos: await $axios.$get(`/users/puntos/?user=${params.id}`),
      history: await $axios.$get(`/bids/history/?user=${params.id}`),
      attachments: await $axios.$get(`/users/attachments/?user=${params.id}`),
      calls,
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
