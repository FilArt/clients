<template>
  <div>
    <v-data-table
      :loading="loading"
      :headers="headers"
      :items="users"
      :options.sync="options"
      :server-items-length="total"
      :footer-props="{
        itemsPerPageOptions: [10, 50, 100],
        showFirstLastPage: true,
        firstIcon: 'mdi-arrow-collapse-left',
        lastIcon: 'mdi-arrow-collapse-right',
        prevIcon: 'mdi-minus',
        nextIcon: 'mdi-plus',
      }"
      class="elevation-1"
      @update:options="updateQuery"
    >
      <template v-slot:top>
        <v-toolbar dense>
          <v-text-field
            v-model="search"
            :disabled="loading"
            append-icon="mdi-database-search"
            label="Search"
            single-line
            hide-details
            @click:append="updateQuery({ search: search })"
            @keydown.enter="updateQuery({ search: search })"
          />

          <v-overflow-btn
            v-if="showFilters"
            v-model="userType"
            :disabled="loading"
            :items="[
              {
                text: 'Clientes',
                value: 'clients',
              },
              {
                text: 'Leeds',
                value: 'leeds',
              },
            ]"
            dense
            hide-details
            class="text-center pa-3"
            label="Tipo de usuario"
            @change="updateQuery({ [userType]: true, [userType === 'clients' ? 'leeds' : 'clients']: false })"
          />

          <v-spacer />

          <v-simple-checkbox
            v-model="onlyNewMessages"
            class="text-center"
            on-icon="mdi-message-plus"
            off-icon="mdi-message-minus"
            color="red"
            @input="updateQuery({ onlyNewMessages: onlyNewMessages })"
          />
        </v-toolbar>
      </template>

      <template v-slot:[`item.email`]="{ item }">
        <nuxt-link :to="$route.path.endsWith('/') ? $route.path + item.id : $route.path + '/' + item.id">
          {{ item.email }}
        </nuxt-link>
      </template>

      <template v-slot:[`item.new_messages_count`]="{ item }">
        <v-badge :content="item.new_messages_count" :value="item.new_messages_count" color="error" overlap>
          <v-btn icon @click="openChat(item)">
            <v-icon>mdi-email</v-icon>
          </v-btn>
        </v-badge>
      </template>

      <template v-if="$auth.user.role === 'admin'" v-slot:[`item.actions`]="{ item }">
        <v-btn icon @click="deleteUser(item)">
          <v-icon color="error">mdi-trash-can-outline</v-icon>
        </v-btn>
      </template>
    </v-data-table>

    <chat
      v-if="$store.state.chat.participant"
      :show-launcher="false"
      is-chat-open-default
      close-socket-on-exit
      @close-chat="fetchUsers"
    />
  </div>
</template>

<script>
export default {
  name: 'UsersTable',
  components: {
    Chat: () => import('~/components/chat/Chat'),
  },
  props: {
    showFilters: {
      type: Boolean,
      default: false,
    },
    headers: {
      type: Array,
      default: () => [
        {
          text: 'ID',
          value: 'id',
        },
        {
          text: 'Email',
          value: 'email',
        },
        {
          text: 'Phone',
          value: 'phone',
        },
        {
          text: 'First name',
          value: 'first_name',
        },
        {
          text: 'Last name',
          value: 'last_name',
        },
        {
          text: 'Date joined',
          value: 'date_joined',
          sortable: false,
        },
        {
          text: 'Last login',
          value: 'last_login',
          sortable: false,
        },
        {
          text: 'Bids',
          value: 'bids_count',
          sortable: false,
        },
        {
          text: 'Nuevo mensajes',
          value: 'new_messages_count',
          sortable: false,
        },
        {
          value: 'actions',
          sortable: false,
        },
      ],
    },
  },
  data() {
    const q = this.$route.query
    return {
      search: '',
      userType: q.clients ? 'clients' : q.leeds ? 'leeds' : null,
      users: [],
      loading: false,
      total: 0,
      options: {
        page: 1,
      },
      onlyNewMessages: false,
      query: { support: this.$route.name === 'support' },
    }
  },
  methods: {
    fetchUsers() {
      return new Promise((resolve, reject) => {
        this.loading = true
        const options = this.options
        const query = {
          page: options.page,
          itemsPerPage: options.itemsPerPage,
          ordering: (options.sortDesc[0] === false ? '-' : '') + options.sortBy,
          ...this.query,
        }
        this.$axios
          .$get(
            'users/users/?' +
              Object.keys(query)
                .filter((k) => query[k])
                .map((k) => {
                  const value = query[k]
                  return value instanceof Array ? `${k}=${value.join()}` : `${k}=${value}`
                })
                .join('&'),
          )
          .then((data) => {
            this.users = data.results
            this.total = data.count
            resolve()
          })
          .catch((e) => reject(e))
          .finally(() => (this.loading = false))
      })
    },
    updateQuery(options) {
      for (const key in options) {
        this.query[key] = options[key]
      }
      this.fetchUsers()
    },
    openChat(user) {
      const options = {
        participant: {
          id: user.id,
          name: user.fullname,
        },
        openChat: true,
      }
      this.$store.dispatch('chat/fetchParticipant', options)
    },
    async deleteUser(user) {
      const isConfirm = await this.$swal({
        title: `Eliminar usuario ${user.fullname || user.email || user.id}?`,
        icon: 'warning',
        buttons: true,
        dangerMode: true,
      })

      if (!isConfirm) return

      try {
        await this.$axios.$delete(`users/manage_users/${user.id}/`)
        await this.fetchUsers()
      } catch (e) {
        await this.$swal({ title: 'Error', text: JSON.stringify(e.response.data), icon: 'error' })
      }
    },
  },
}
</script>
