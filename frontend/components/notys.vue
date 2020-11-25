<template>
  <v-menu offset-y :close-on-content-click="false">
    <template v-slot:activator="{ on, attrs }">
      <v-badge :content="unread" :value="unread" color="error" overlap>
        <v-btn icon :loading="loading" color="primary" v-bind="attrs" v-on="on">
          <v-icon>mdi-eye</v-icon>
        </v-btn>
      </v-badge>
    </template>

    <v-card>
      <v-virtual-scroll :bench="10" :items="notys" height="300" item-height="64" width="600">
        <template v-slot:default="{ item }">
          <v-list-item two-line nuxt :to="getUrl(item)" exact>
            <v-list-item-content>
              <v-list-item-title>
                {{ $dateFns.format(new Date(item.timestamp), 'dd/MM/yyyy HH:mm') }}
              </v-list-item-title>
              <v-list-item-subtitle>{{ item.author }} {{ getActionWord(item) }}</v-list-item-subtitle>
            </v-list-item-content>

            <!--            <v-list-item-action>-->
            <!--              <v-btn small icon color="warning" @click="toggleUnread(item)">-->
            <!--                <v-icon small>-->
            <!--                  {{ item.unread ? 'mdi-check' : 'mdi-cancel' }}-->
            <!--                </v-icon>-->
            <!--              </v-btn>-->
            <!--            </v-list-item-action>-->

            <v-list-item-action>
              <v-btn small icon color="error" @click.prevent="deleteNoty(item.id)">
                <v-icon small>mdi-trash-can-outline</v-icon>
              </v-btn>
            </v-list-item-action>
          </v-list-item>

          <v-divider></v-divider>
        </template>
      </v-virtual-scroll>
    </v-card>
  </v-menu>
</template>

<script>
export default {
  name: 'Notys',
  data() {
    return {
      loading: false,
      notys: [],
      refreshInterval: null,
    }
  },
  computed: {
    unread() {
      return this.notys.filter(({ unread }) => unread).length
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
      this.loading = true
      try {
        await this.$axios.$delete(`users/notys/${id}/`)
        await this.refresh()
        this.$toast.global.done()
      } finally {
        this.loading = false
      }
    },
    // async toggleUnread(noty) {
    //   if (noty.unread) {
    //     await this.$axios.$post(`users/notys/${noty.id}/mark_read/`)
    //   } else {
    //     await this.$axios.$post(`users/notys/${noty.id}/mark_unread/`)
    //   }
    //   await this.refresh()
    // },
    async refresh() {
      this.loading = true
      this.notys = await this.$axios.$get('users/notys/?')
      this.loading = false
    },
    getUrl({ verb, target_object_id, actor_object_id }) {
      if (verb !== 'new_attachment') return
      return `/admin/tramitacion/${target_object_id}?highligh_item=attachment&highligh_item_id=${actor_object_id}`
    },
    getActionWord({ verb, actor_object_id }) {
      return verb === 'new_attachment' ? `agregó archivo ${actor_object_id}` : verb
    },
    getIcon({ verb }) {
      return verb === 'new_attachment' ? 'mdi-file' : 'NOICON'
    },
  },
}
</script>
