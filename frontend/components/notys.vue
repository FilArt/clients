<template>
  <v-dialog v-model="dialog" max-width="750">
    <template v-slot:activator="{ on }">
      <v-badge :content="unread" :value="unread" color="error" overlap>
        <v-btn icon :loading="loading" color="primary" v-on="on">
          <v-icon>mdi-eye</v-icon>
        </v-btn>
      </v-badge>
    </template>

    <v-card>
      <v-card-title>
        <v-row align="center">
          <v-col>Notificaciones</v-col>

          <v-spacer />

          <v-col class="flex-grow-0">
            <close-button @click="dialog = false" />
          </v-col>
        </v-row>
      </v-card-title>

      <v-card-text>
        <v-list v-for="noty in notys" :key="noty.id">
          <v-list-item>
            <v-row align="center">
              <v-col class="flex-grow-0">
                <v-list-item-icon>
                  <v-icon :color="noty.level">{{ getIcon(noty) }}</v-icon>
                </v-list-item-icon>
              </v-col>
              <v-col>
                {{ $dateFns.format(new Date(noty.timestamp), 'dd/MM/yyyy HH:mm') }}
              </v-col>
              <v-col> {{ noty.author }} {{ getActionWord(noty) }} </v-col>
              <v-col>
                <v-btn nuxt :to="getUrl(noty)">
                  <v-icon>mdi-arrow-right</v-icon>
                </v-btn>
              </v-col>
              <v-col class="flex-grow-0">
                <v-btn icon color="warning" @click="toggleUnread(noty)">
                  <v-icon>
                    {{ noty.unread ? 'mdi-check' : 'mdi-cancel' }}
                  </v-icon>
                </v-btn>

                <v-btn icon color="error" @click="deleteNoty(noty.id)">
                  <v-icon>mdi-trash-can-outline</v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import CloseButton from '@/components/buttons/closeButton'

export default {
  name: 'Notys',
  components: { CloseButton },
  data() {
    return {
      loading: false,
      dialog: false,
      notys: [],
      refreshInterval: null,
    }
  },
  computed: {
    unread() {
      return this.notys.filter((noty) => noty.unread).length
    },
  },
  async mounted() {
    await this.refresh()
    clearInterval(this.refreshInterval)
    this.refreshInterval = setInterval(this.refresh, 50000)
  },
  async beforeDestroy() {
    clearInterval(this.refreshInterval)
  },
  methods: {
    async deleteNoty(id) {
      await this.$axios.$delete(`users/notys/${id}/`)
      await this.refresh()
    },
    async toggleUnread(noty) {
      if (noty.unread) {
        await this.$axios.$post(`users/notys/${noty.id}/mark_read/`)
      } else {
        await this.$axios.$post(`users/notys/${noty.id}/mark_unread/`)
      }
      await this.refresh()
    },
    async refresh() {
      this.loading = true
      this.notys = await this.$axios.$get('users/notys/?')
      this.loading = false
    },
    getUrl(noty) {
      if (noty.verb === 'new_attachment') {
        return `/admin/tramitacion/${noty.target_object_id}?highligh_item=attachment&highligh_item_id=${noty.actor_object_id}`
      }
    },
    getActionWord(noty) {
      if (noty.verb === 'new_attachment') {
        return 'added attachment'
      }
      return noty.verb
    },
    getIcon(noty) {
      if (noty.verb === 'new_attachment') {
        return 'mdi-file'
      }
      return 'NOICON'
    },
  },
}
</script>
