<template>
  <div>
    <v-data-table :headers="headers" :items="filteredUsers" :search.sync="search">
      <template v-slot:top>
        <v-row>
          <v-col>
            <v-text-field v-model="search" append-icon="mdi-database-search" label="Search" single-line hide-details />
          </v-col>
          <v-spacer />
          <v-col>
            <v-checkbox
              v-if="$auth.user && $auth.user.role === 'admin'"
              v-model="filterByNewMessages"
              label="Nuevo mensajes"
            />
          </v-col>
        </v-row>
      </template>

      <template v-slot:[`item.fullname`]="{ item }">
        <nuxt-link :to="$route.path.endsWith('/') ? $route.path + item.id : $route.path + '/' + item.id">
          {{ item.fullname }}
        </nuxt-link>
      </template>

      <template v-slot:[`item.new_messages_count`]="{ item }">
        <v-badge :content="item.new_messages_count" :value="item.new_messages_count" color="error" overlap>
          <v-btn icon @click="openChat(item)">
            <v-icon>mdi-email</v-icon>
          </v-btn>
        </v-badge>
      </template>
    </v-data-table>

    <chat
      v-if="$store.state.chat.participant"
      :show-launcher="false"
      is-chat-open-default
      close-socket-on-exit
      @close-chat="$emit('refresh')"
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
    headers: {
      type: Array,
      default: () => [
        {
          text: 'ID',
          value: 'id',
        },
        {
          text: 'Nombre',
          value: 'fullname',
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
        },
        {
          text: 'Last login',
          value: 'last_login',
        },
        {
          text: 'Bids',
          value: 'bids_count',
        },
        {
          text: 'Nuevo mensajes',
          value: 'new_messages_count',
        },
      ],
    },
    users: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      search: '',
      filterByNewMessages: false,
    }
  },
  computed: {
    filteredUsers() {
      return this.filterByNewMessages ? this.users.filter((u) => u.new_messages_count > 0) : this.users
    },
  },
  methods: {
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
  },
}
</script>
