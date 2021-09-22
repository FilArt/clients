<template>
  <v-card flat>
    <v-toolbar dense>
      <v-toolbar-title>
        <v-btn icon color="error" @click="$router.back()">
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        {{ user.fullname }}
      </v-toolbar-title>

      <v-spacer />

      <v-toolbar-items>
        <v-btn color="error" @click="moveToKo">Mover a papellera</v-btn>
      </v-toolbar-items>
    </v-toolbar>

    <v-card-text>
      <user-detail-data :user-id="$route.params.id" @user-updated="refresh" />

      <v-dialog v-model="userHistoryDialog" scrollable max-width="750px">
        <template v-slot:activator="{ on }">
          <v-btn block color="primary" :disabled="!userHistory || !userHistory.length" v-on="on">
            <v-icon left>mdi-eye</v-icon>
            Ver el historial del usuario
          </v-btn>
        </template>
        <v-card>
          <v-card-title>
            Cambias
            <v-spacer />
            <close-button @click="userHistoryDialog = false" />
          </v-card-title>

          <v-divider></v-divider>

          <v-card-text style="height: 500px">
            <v-list>
              <v-list-item v-for="item in userHistory" :key="item.id">
                <v-list-item-content>
                  <v-list-item-title>
                    <v-row>
                      <v-col> ID: {{ item.id }} </v-col>
                      <v-col>
                        <caption>
                          {{
                            formatDate(item.requested_at)
                          }}
                        </caption>
                      </v-col>
                      <v-col>
                        <nuxt-link :to="'/admin/usuarios/' + item.user">{{ item.username_persistent }}</nuxt-link>
                      </v-col>
                    </v-row>
                  </v-list-item-title>
                  <p
                    v-for="(subitem, idx) in formatJson(item.data)"
                    :key="idx"
                    :style="subitem.startsWith('\t') ? 'text-indent: 1em' : ''"
                    class="truncate"
                  >
                    {{ subitem }}
                  </p>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-dialog>
    </v-card-text>

    <v-card-text>
      <v-tabs v-model="tabs" centered>
        <v-tab>Tramitación</v-tab>
        <v-tab>Facturacion</v-tab>
        <v-tab :disabled="!bids.length">Solicitud ({{ bids.length }})</v-tab>
        <v-tab :disabled="!calls.length"> Llamadas ({{ calls.length }}) </v-tab>
        <v-tab :disabled="!history.length">Historia ({{ history.length }})</v-tab>
        <v-tab :disabled="!puntos.length"> Puntos suministros ({{ puntos.length }}) </v-tab>

        <v-tabs-items v-model="tabs">
          <v-tab-item>
            <solicitudes-process
              allow-delete
              :user="user"
              @bid-added="refresh"
              @tramitate="refresh"
              @punto-deleted="refresh"
              @bid-deleted="refresh"
              @punto-updated="refresh"
            />
          </v-tab-item>
          <v-tab-item>
            <solicitudes-process
              allow-delete
              :user="user"
              facturacion
              @bid-added="refresh"
              @tramitate="refresh"
              @punto-deleted="refresh"
              @bid-deleted="refresh"
              @punto-updated="refresh"
            />
          </v-tab-item>
          <v-tab-item>
            <v-container>
              <v-toolbar>
                <v-row align="center">
                  <v-col>Solicitudes</v-col>
                  <v-spacer />
                  <v-col>
                    <add-new-bid-dialog :user-id="$route.params.id" label="Añadir nuevo solicitud" />
                  </v-col>
                </v-row>
              </v-toolbar>

              <v-list three-line subheader nav shaped>
                <v-list-item v-for="bid in bids" :key="bid.id" nuxt :to="`/bids/${bid.id}`">
                  <v-list-item-content>
                    <v-list-item-title v-text="bid.offer_name" />
                    <v-list-item-subtitle v-text="'id: ' + bid.id" />
                    <v-list-item-subtitle v-text="bid.fecha_firma" />
                  </v-list-item-content>

                  <v-list-item-content>
                    {{ bid.status }}
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-container>
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

          <v-tab-item>
            <history-list v-if="history.length" :history="history" />
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
import { mapState } from 'vuex'
import { format } from 'date-fns'
export default {
  components: {
    SolicitudesProcess: () => import('@/components/SolicitudesProcess'),
    AddNewBidDialog: () => import('@/components/dialogs/AddNewBidDialog'),
    Chat: () => import('~/components/chat/Chat'),
    PuntosList: () => import('~/components/puntos/PuntosList'),
    HistoryList: () => import('~/components/history/HistoryList'),
    UserDetailData: () => import('@/components/forms/UserDetailData'),
    CloseButton: () => import('@/components/buttons/closeButton.vue'),
  },
  async asyncData({ params, $axios }) {
    const user = await $axios.$get(`/users/users/${params.id}/`)

    const phoneNumbers = [user.phone, user['phone_city']]
    let calls = []
    if (phoneNumbers.length) {
      calls = await $axios.$get(`users/calls/${params.id}`)
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
      puntos: await $axios.$get(`/users/puntos/?user=${params.id}`),
      history: await $axios.$get(`/bids/history/?user=${params.id}`),
      userHistory: await $axios.$get(`/users/manage_users/${params.id}/history/`),
      tabs: null,
      userHistoryDialog: false,
    }
  },
  computed: mapState({ bids: (state) => state.bids.bids }),
  methods: {
    async moveToKo() {
      const confirmed = await this.$swal({
        title: `¿Estás seguro de que quieres hacer esto?`,
        icon: 'warning',
        buttons: true,
        dangerMode: true,
      })
      if (!confirmed) return
      await this.$axios.$patch(`users/users/${this.user.id}/`, { ko: true })
      await this.$router.push(`/admin/ko/${this.user.id}`)
    },
    formatDate(dateStr) {
      return format(new Date(dateStr), 'dd/MM/yyyy HH:mm')
    },
    formatJson(obj) {
      const subitems = []
      Object.keys(obj).forEach((key) => {
        const val = obj[key]
        if (String(val).includes('\n')) {
          const lines = val.split('\n')
          subitems.push(`${key}:`)
          lines.forEach((line) => {
            subitems.push('\t' + line)
          })
        } else {
          subitems.push(`${key}: ${val}`)
        }
        return `${key}: ${obj[key]}`
      })
      return subitems
    },
    async refresh() {
      const user = await this.$axios.$get(`/users/users/${this.$route.params.id}/`)
      await this.$store.dispatch('bids/fetchBids', { params: `user=${user.id}` })
      this.userHistory = await this.$axios.$get(`/users/manage_users/${user.id}/history/`)
      this.user = user
    },
    async fetchPuntos() {
      this.puntos = await this.$axios.$get(`/users/puntos/?user=${this.$route.params.id}`)
    },
  },
}
</script>
