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
      @update:options="fetchUsers"
    >
      <template v-slot:top>
        <div class="pa-3">
          <v-row align="center" class="elevation-1 pa-3 flex-wrap" justify="space-around">
            <v-col cols="11">
              <v-text-field
                v-model="search"
                :disabled="loading"
                append-icon="mdi-database-search"
                label="Buscar"
                hint="buscar por nombre, número de teléfono o correo electrónico"
                persistent-hint
                single-line
                @click:append="updateQuery({ search: search })"
                @keydown.enter="updateQuery({ search: search })"
              />
            </v-col>

            <v-col cols="1" lg="1" xl="1" md="1" sm="1">
              <v-tooltip v-if="!hideChat && !isSupport" bottom>
                <template v-slot:activator="{ on }">
                  <v-simple-checkbox
                    v-model="onlyNewMessages"
                    class="text-center"
                    on-icon="mdi-message-plus"
                    off-icon="mdi-message-minus"
                    color="red"
                    v-on="on"
                    @input="updateQuery({ onlyNewMessages: onlyNewMessages })"
                  />
                </template>
                <span>Filtro por nuevo mensajes</span>
              </v-tooltip>
            </v-col>

            <v-col
              v-if="headers.some((h) => h.value === 'affiliate')"
              :cols="flexs.cols"
              :xl="flexs.xl"
              :lg="flexs.lg"
              :md="flexs.md"
              :xs="flexs.xs"
            >
              <v-select
                v-model="query.source"
                label="Origin"
                :items="[
                  {
                    text: 'Default',
                    value: 'default',
                  },
                  {
                    text: 'Call&Visit',
                    value: 'call_n_visit',
                  },
                ]"
                clearable
                @change="updateQuery({ source: $event })"
              />
            </v-col>

            <v-col :cols="flexs.cols" :xl="flexs.xl" :lg="flexs.lg" :md="flexs.md" :xs="flexs.xs">
              <v-select
                v-if="headers.some((h) => h.value === 'responsible')"
                v-model="query.responsible"
                label="Responsable"
                :items="responsibles"
                item-text="fullname"
                item-value="id"
                clearable
                @change="updateQuery({ responsible: $event })"
              />
            </v-col>

            <v-col :cols="flexs.cols" :xl="flexs.xl" :lg="flexs.lg" :md="flexs.md" :xs="flexs.xs">
              <v-overflow-btn
                v-if="showFilters"
                v-model="role"
                :disabled="loading"
                :items="userRoles"
                hint="los clientes son los que firmaron un contrato con nosotros"
                persistent-hint
                class="text-center pa-3"
                label="Tipo de usuario"
                @change="clientRole ? null : updateQuery({ role: role })"
              >
                <template v-slot:append>
                  <add-new-employee @added="fetchUsers" />
                </template>
              </v-overflow-btn>
            </v-col>

            <v-col
              v-if="showDateFilters || headers.some((h) => h.value === 'date_joined_date')"
              :cols="flexs.cols"
              :xl="flexs.xl"
              :lg="flexs.lg"
              :md="flexs.md"
              :xs="flexs.xs"
            >
              <vue-ctk-date-time-picker
                v-model="dateJoinedFilter"
                :label="showDateFilters ? 'Fecha firma' : 'Fecha de registro'"
                format="YYYY-MM-DD HH:mm"
                formatted="DD/MM/YYYY HH:mm"
                range
                color="purple"
                :dark="$vuetify.theme.isDark"
                @input="updateDateJoinedFilter"
              />
            </v-col>
          </v-row>
        </div>
      </template>

      <template v-if="useFullName" v-slot:[`item.fullname`]="{ item }">
        <nuxt-link :to="getDetailUrl(item.id)">
          {{ item.fullname }}
        </nuxt-link>
      </template>

      <template v-else v-slot:[`item.email`]="{ item }">
        <nuxt-link :to="getDetailUrl(item.id)">
          {{ item.email }}
        </nuxt-link>
      </template>

      <template v-if="!hideChat" v-slot:[`item.new_messages_count`]="{ item }">
        <v-badge :content="item.new_messages_count" :value="item.new_messages_count" color="error" overlap>
          <v-btn icon @click="openChat(item)">
            <v-icon>mdi-email</v-icon>
          </v-btn>
        </v-badge>
      </template>

      <template v-if="allowDelete && $auth.user.role === 'admin'" v-slot:[`item.actions`]="{ item }">
        <delete-button @click="deleteUser(item)" />
      </template>

      <template v-if="$auth.user.role === 'admin'" v-slot:[`item.responsible`]="{ item }">
        <v-edit-dialog
          :return-value.sync="item.responsible"
          large
          @save="editResponsible"
          @open="reserved_userId = item.id"
        >
          {{ item.responsible }}
          <template v-slot:input>
            <v-list dense>
              <v-subheader>Agentes</v-subheader>
              <v-list-item-group v-model="reserved_responsible" color="primary">
                <v-list-item :value="null">
                  <v-list-item-title>-</v-list-item-title>
                </v-list-item>

                <v-list-item v-for="resp in responsibles" :key="resp.id" :value="resp.id">
                  <v-list-item-content>
                    <v-list-item-title>{{ resp.fullname }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </template>
        </v-edit-dialog>
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
import constants from '@/lib/constants'
import { mapState } from 'vuex'
export default {
  name: 'UsersTable',
  components: {
    AddNewEmployee: () => import('@/components/forms/AddNewEmployee'),
    DeleteButton: () => import('@/components/buttons/deleteButton'),
    Chat: () => import('~/components/chat/Chat'),
  },
  props: {
    filtersToShow: {
      type: Array,
      default: () => [],
    },
    useFullName: {
      type: Boolean,
      default: false,
    },
    hideChat: {
      type: Boolean,
      default: false,
    },
    allowDelete: {
      type: Boolean,
      default: false,
    },
    showFilters: {
      type: Boolean,
      default: false,
    },
    showDateFilters: {
      type: Boolean,
      default: false,
    },
    isSupport: {
      type: Boolean,
      default: false,
    },
    clientRole: {
      type: String,
      default: null,
    },
    defaultHeaders: {
      type: Array,
      default: () => [
        {
          text: 'ID',
          value: 'id',
        },
        {
          text: 'Fecha de registro',
          value: 'date_joined_date',
        },
        {
          text: 'Email',
          value: 'email',
        },
        {
          text: 'Telefono',
          value: 'phone',
        },
        {
          text: 'Nombre/Razon social',
          value: 'fullname',
        },
        {
          text: 'Ultima entrada',
          value: 'last_login',
        },
        {
          text: 'Cartera',
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
    additionalHeaders: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      flexs: { cols: 12, xl: 3, lg: 3, md: 3, sm: 3, xs: 12 },
      dateJoinedFilter: null,
      userRoles: Object.values(constants.userRoles),
      search: '',
      role: 'admin',
      users: [],
      loading: false,
      total: 0,
      options: { page: 1 },
      onlyNewMessages: false,
      query: { is_support: this.isSupport },
      reserved_responsible: null,
      reserved_userId: null,
    }
  },
  computed: {
    ...mapState({ responsibles: (state) => state.responsibles }),
    headers() {
      const result = this.defaultHeaders
      this.additionalHeaders.forEach((header) => {
        result.splice(header.index, 0, header.value)
      })
      return result
    },
  },
  async created() {
    if (this.headers.some((header) => header.value === 'responsible') && !this.responsibles.length) {
      const users = (await this.$axios.$get('users/users/?role=agent&fields=id,fullname&itemsPerPage=100')).results
      this.$store.commit('setResponsibles', users)
    }
    if (!this.clientRole && this.role) this.query.role = this.role
  },
  methods: {
    async editResponsible() {
      await this.$axios.$patch(`users/manage_users/${this.reserved_userId}/`, {
        responsible: this.reserved_responsible || null,
      })
      await this.fetchUsers()
    },

    getDetailUrl(userId) {
      let detailUrl
      if (this.isSupport) {
        detailUrl = this.$auth.user.role === 'agent' ? `/agente/${userId}` : `/support/${userId}`
      } else {
        detailUrl = `${this.$route.path}/${userId}`
      }
      return detailUrl
    },

    // other
    fetchUsers() {
      return new Promise((resolve, reject) => {
        this.loading = true
        const { options } = this
        const query = {
          page: options.page,
          itemsPerPage: options.itemsPerPage,
          ordering: options.sortBy
            .map(
              (sortBy, idx) =>
                (options.sortDesc[idx] ? '+' : '-') + (sortBy === 'date_joined_date' ? 'date_joined' : sortBy),
            )
            .join(),
          fields: this.headers.map((header) => header.value).join(),
          ...this.query,
        }
        if (this.clientRole) {
          query.client_role = this.clientRole
          query.role__isnull = true
        }

        this.$axios
          .$get(
            `users/users/?${Object.keys(query)
              .filter((k) => query[k])
              .map((k) => {
                const value = query[k]
                return value instanceof Array ? `${k}=${value.join()}` : `${k}=${value}`
              })
              .join('&')}`,
          )
          .then((data) => {
            this.users = data.results
            this.total = data.count
            resolve()
          })
          .catch((e) => reject(e))
          .finally(() => {
            this.loading = false
          })
      })
    },
    updateDateJoinedFilter(dates) {
      if (dates && dates.start && dates.end) {
        this.updateQuery({ date_joined__range: `${dates.start},${dates.end}` })
      } else {
        this.updateQuery({ date_joined__range: null })
      }
    },
    updateQuery(options) {
      Object.keys(options).forEach((key) => {
        const value = options[key]
        if (value) {
          this.query[key] = options[key]
        } else {
          delete this.query[key]
        }
      })
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
