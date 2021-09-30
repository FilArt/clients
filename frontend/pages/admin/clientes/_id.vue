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
        <v-select :value="status" solo :items="userStatuses" @change="changeStatus" />
        <v-btn color="error" @click="moveToKo">Mover a papellera</v-btn>
      </v-toolbar-items>
    </v-toolbar>

    <v-card-text>
      <user-detail-data :user-id="$route.params.id" @user-updated="refresh" />
    </v-card-text>

    <v-card-text>
      <v-tabs v-model="tabs" centered>
        <v-tab>Tramitación</v-tab>
        <v-tab>Facturacion</v-tab>
        <v-tab :disabled="!bids.length">Solicitud ({{ bids.length }})</v-tab>
        <v-tab :disabled="!calls.length"> Llamadas ({{ calls.length }}) </v-tab>
        <v-tab :disabled="!puntos.length"> Puntos suministros ({{ puntos.length }}) </v-tab>
        <v-tab>Call-Visit</v-tab>

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
            <puntos-list :puntos="puntos" @punto-updated="fetchPuntos" />
          </v-tab-item>

          <v-tab-item>
            <ficha :card-id="user.call_visit_id" />
          </v-tab-item>
        </v-tabs-items>
      </v-tabs>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapState } from 'vuex'
import constants from '../../../lib/constants'

export default {
  components: {
    SolicitudesProcess: () => import('@/components/SolicitudesProcess'),
    AddNewBidDialog: () => import('@/components/dialogs/AddNewBidDialog'),
    PuntosList: () => import('~/components/puntos/PuntosList'),
    UserDetailData: () => import('@/components/forms/UserDetailData'),
    Ficha: () => import('../../../components/Ficha.vue'),
  },
  async asyncData({ params, $axios }) {
    const user = await $axios.$get(`/users/users/${params.id}/`)

    const phoneNumbers = [user.phone, user['phone_city']]
    let calls = []
    if (phoneNumbers.length) {
      calls = await $axios.$get(`users/calls/${params.id}`)
    }

    return {
      userStatuses: constants.userStatuses,
      user,
      calls,
      puntos: await $axios.$get(`/users/puntos/?user=${params.id}`),
      tabs: null,
    }
  },
  computed: {
    ...mapState({ bids: (state) => state.bids.bids }),
    status() {
      return typeof this.user.status === 'number' ? String(this.user.status) : this.user.status
    },
  },
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
    async refresh() {
      const user = await this.$axios.$get(`/users/users/${this.$route.params.id}/`)
      await this.$store.dispatch('bids/fetchBids', { params: `user=${user.id}` })
      this.user = user
    },
    async fetchPuntos() {
      this.puntos = await this.$axios.$get(`/users/puntos/?user=${this.$route.params.id}`)
    },
    async changeStatus(status) {
      try {
        const user = await this.$axios.$patch(`users/users/${this.user.id}/`, { status })
        this.user = user
        this.$toast.global.done()
      } catch (e) {
        const errText = e.response.data.status[0]
        await this.$swal({ title: 'Error', text: errText, icon: 'error' })
      }
    },
  },
}
</script>
