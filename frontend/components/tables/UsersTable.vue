<template>
  <div>
    <v-snackbar v-model="actionsSnackbar" :timeout="-1">
      <v-card>
        <v-card-title>
          <v-toolbar>
            <v-toolbar-title>{{ selected.length }} clientes </v-toolbar-title>
            <v-spacer />
            <v-toolbar-items>
              <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    icon
                    color="#004680"
                    v-bind="attrs"
                    e
                    v-on="on"
                    @click="
                      uploadToCallVisitDialog = true
                      actionsSnackbar = false
                    "
                  >
                    <v-icon>mdi-cloud-upload</v-icon>
                  </v-btn>
                </template>
                <span>Enviar en Call&Visit.</span>
              </v-tooltip>
            </v-toolbar-items>
          </v-toolbar>
        </v-card-title>

        <v-card-text>
          <v-virtual-scroll :items="selected" height="300" item-height="64">
            <template v-slot:default="{ item }">
              <v-list-item :key="item.id">
                <v-list-item-content>
                  <v-list-item-subtitle>{{ item.id }}</v-list-item-subtitle>
                  <v-list-item-title>{{ item.fullname }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-divider></v-divider>
            </template>
          </v-virtual-scroll>
        </v-card-text>
      </v-card>
    </v-snackbar>

    <v-dialog v-model="uploadToCallVisitDialog" persistent>
      <v-card>
        <v-card-title>
          <span> Enviar en Call&Visit </span>
          <v-spacer />
          <close-button
            @click="
              uploadToCallVisitDialog = false
              actionsSnackbar = true
            "
          />
        </v-card-title>
        <v-card-text>
          <v-form @submit.prevent="uploadToCallVisit">
            <cv-user-select v-model="form.manager" type="manager" />
            <cv-user-select v-model="form.operator" type="operator" />
            <cv-user-select v-model="form.tele" type="tele" />
            <v-select v-model="form.status" label="Estado" :items="Object.values(constants.cvStatuses)" />
            <submit-button label="Enviar" block />
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>

    <v-data-table
      :show-select="selectable"
      :loading="loading"
      :headers="activeHeaders"
      :items="users"
      :options.sync="query"
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
      @toggle-select-all="onSelect"
      @item-selected="onSelect"
    >
      <template v-slot:top>
        <div class="pa-3">
          <v-row align="center" class="elevation-1 pa-3 flex-wrap" justify="space-around">
            <v-col :cols="showFilters ? 8 : showChat && !isSupport ? 11 : 12">
              <v-text-field
                v-model="search"
                :disabled="loading"
                append-icon="mdi-database-search"
                label="Buscar"
                hint="Buscar por id, cups, CIF/DNI, número de teléfono o correo electrónico"
                persistent-hint
                single-line
                @click:append="updateQuery({ search: search })"
                @keydown.enter="updateQuery({ search: search })"
              />
            </v-col>

            <v-col v-if="showFilters" :cols="flexs.cols" :xl="flexs.xl" :lg="flexs.lg" :md="flexs.md" :xs="flexs.xs">
              <v-overflow-btn
                v-model="role"
                :disabled="loading"
                :items="userRoles"
                hint="los clientes son los que firmaron un contrato con nosotros"
                persistent-hint
                class="text-center pa-3"
                label="Tipo de usuario"
                @change="updateQuery({ role: role })"
              >
                <template v-slot:append>
                  <add-new-employee @added="fetchUsers" />
                </template>
              </v-overflow-btn>
            </v-col>

            <v-col v-if="showChat && !isSupport" cols="1" lg="1" xl="1" md="1" sm="1">
              <v-tooltip bottom>
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

            <!--            <v-col-->
            <!--              v-if="headers.some((h) => h.value === 'affiliate')"-->
            <!--              :cols="flexs.cols"-->
            <!--              :xl="flexs.xl"-->
            <!--              :lg="flexs.lg"-->
            <!--              :md="flexs.md"-->
            <!--              :xs="flexs.xs"-->
            <!--            >-->
            <!--              <v-select-->
            <!--                v-model="query.source"-->
            <!--                label="Origin"-->
            <!--                :items="[-->
            <!--                  {-->
            <!--                    text: 'Online',-->
            <!--                    value: 'default',-->
            <!--                  },-->
            <!--                  {-->
            <!--                    text: 'Call&Visit',-->
            <!--                    value: 'call_n_visit',-->
            <!--                  },-->
            <!--                ]"-->
            <!--                clearable-->
            <!--                @change="updateQuery({ source: $event })"-->
            <!--              />-->
            <!--            </v-col>-->

            <v-col
              v-if="headers.some((h) => h.includes('responsible'))"
              :cols="flexs.cols"
              :xl="flexs.xl"
              :lg="flexs.lg"
              :md="flexs.md"
              :xs="flexs.xs"
            >
              <v-autocomplete
                v-model="query.responsible__in"
                label="Responsable"
                :items="responsibles"
                multiple
                item-text="fullname"
                item-value="id"
                clearable
                @change="updateQuery({ responsible__in: $event })"
              />
            </v-col>

            <v-col
              v-if="showDateFilters || headers.some((h) => h.includes('date_joined'))"
              :cols="flexs.cols"
              :xl="flexs.xl"
              :lg="flexs.lg"
              :md="flexs.md"
              :xs="flexs.xs"
            >
              <date-time-filter
                v-model="dateJoinedFilter"
                label="Fecha de registro"
                range
                @input="updateDateJoinedFilter"
              />
            </v-col>

            <v-col
              v-if="headers.some((h) => h === 'fecha_firma')"
              :cols="flexs.cols"
              :xl="flexs.xl"
              :lg="flexs.lg"
              :md="flexs.md"
              :xs="flexs.xs"
            >
              <date-time-filter
                v-model="fechaFirmaFilter"
                label="Fecha de firma"
                format="YYYY-MM-DD"
                formatted="DD/MM/YYYY"
                range
                @input="updateFechaFirmaFilter"
              />
            </v-col>

            <v-col
              v-if="headers.some((h) => h === 'status')"
              :cols="flexs.cols"
              :xl="flexs.xl"
              :lg="flexs.lg"
              :md="flexs.md"
              :xs="flexs.xs"
            >
              <v-select
                v-model="query.statuses_in"
                label="Estado"
                :items="statuses"
                multiple
                chips
                deletable-chips
                small-chips
                clearable
                @change="updateQuery({ statuses_in: $event })"
              />
            </v-col>

            <template v-if="headers.some((h) => h === 'status') && isSupport">
              <v-col
                v-for="q in [
                  { text: 'Doc', value: 'bids__doc' },
                  { text: 'Scoring', value: 'bids__scoring' },
                  { text: 'Llamada', value: 'bids__call' },
                  { text: 'Estado de oferta', value: 'bids__offer_status' },
                ]"
                :key="q.value"
              >
                <v-select
                  v-model="query[q.value]"
                  :label="q.text"
                  clearable
                  :items="q.value === 'bids__offer_status' ? offerStatusItems : booleanItems"
                  @change="
                    query[q.value] === 'None'
                      ? updateQuery({ [`${q.value}__isnull`]: 'true', [q.value]: null })
                      : updateQuery({ [`${q.value}__isnull`]: null, [q.value]: query[q.value] })
                  "
                />
              </v-col>
            </template>
          </v-row>
        </div>
      </template>

      <template v-if="useFullName" v-slot:[`item.fullname`]="{ item }">
        <v-row v-if="detailUrl" align="center">
          <v-col>
            <nuxt-link :to="getDetailUrl(item.id)">
              {{ item.fullname }}
            </nuxt-link>
          </v-col>

          <v-col>
            <v-btn icon x-small link :to="getDetailUrl(item.id)" target="_blank">
              <v-icon>mdi-open-in-new</v-icon>
            </v-btn>
          </v-col>
        </v-row>
        <span v-else>{{ item.fullname }}</span>
      </template>

      <template v-else v-slot:[`item.email`]="{ item }">
        <nuxt-link v-if="detailUrl" :to="getDetailUrl(item.id)">
          {{ item.email }}
        </nuxt-link>
        <span v-else>
          {{ item.email }}
        </span>
      </template>

      <template v-if="showChat" v-slot:[`item.new_messages_count`]="{ item }">
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

      <template v-slot:[`item.date_joined`]="{ item }">
        {{ $dateFns.format(new Date(item.date_joined), 'yyyy-MM-dd HH:mm') }}
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
    CvUserSelect: () => import('@/components/cv_components/selects/cvUserSelect'),
    CloseButton: () => import('~/components/buttons/closeButton'),
    SubmitButton: () => import('~/components/buttons/submitButton'),
    AddNewEmployee: () => import('@/components/forms/AddNewEmployee'),
    DeleteButton: () => import('@/components/buttons/deleteButton'),
    Chat: () => import('~/components/chat/Chat'),
    DateTimeFilter: () => import('~/components/DateTimeFilter'),
  },
  props: {
    selectable: {
      type: Boolean,
      default: false,
    },
    statuses: {
      type: Array,
      default: () => [],
    },
    listUrl: {
      type: String,
      default: 'users/users',
    },
    detailUrl: {
      type: String,
      default: '/admin/tramitacion',
    },
    useFullName: {
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
    defaultRole: {
      type: String,
      default: null,
    },
    headers: {
      type: Array,
      default: () => [],
    },
    responsible: {
      type: [String, Number],
      default: 0,
    },
  },
  data() {
    const query = this.$route.query
    let dateJoinedFilter = query.date_joined__range || null
    let fechaFirmaFilter = query.fecha_firma__range || null
    if (dateJoinedFilter) {
      try {
        const [start, end] = dateJoinedFilter.split(',')
        dateJoinedFilter = { start: new Date(start), end: new Date(end) }
      } catch (e) {
        console.error(e)
      }
    }
    if (fechaFirmaFilter) {
      try {
        const [start, end] = fechaFirmaFilter.split(',')
        fechaFirmaFilter = { start: new Date(start), end: new Date(end) }
      } catch (e) {
        console.error(e)
      }
    }
    return {
      constants,
      uploadToCallVisitDialog: false,
      actionsSnackbar: false,
      selected: [],
      form: {
        manager: null,
        operator: null,
        tele: null,
        status: null,
      },
      booleanItems: [
        {
          text: 'OK',
          value: 'True',
        },
        {
          text: 'KO',
          value: 'False',
        },
        {
          text: '-',
          value: 'None',
        },
      ],
      offerStatusItems: [
        {
          text: 'FIRMADA',
          value: '0',
        },
        {
          text: 'PTE FIRMAR',
          value: '1',
        },
        {
          text: '-',
          value: 'None',
        },
      ],
      flexs: { cols: 12, xl: 3, lg: 3, md: 3, sm: 3, xs: 12 },
      dateJoinedFilter,
      fechaFirmaFilter,
      userRoles: Object.values(constants.userRoles),
      role: this.defaultRole,
      users: [],
      loading: false,
      total: 0,
      onlyNewMessages: false,
      reserved_responsible: null,
      reserved_userId: null,

      search: query.search || '',
      query: {
        ...query,
        statuses_in: query.statuses_in ? query.statuses_in.split(',') : [],
        mustSort: null,
        multiSort: null,
        bids__call: null,
        bids__doc: null,
        bids__scoring: null,
        responsible: this.responsible ? this.responsible : query.responsible ? parseInt(query.responsible) : null,
        page: query.page ? parseInt(query.page) : 1,
        itemsPerPage: query.itemsPerPage ? parseInt(query.itemsPerPage) : 10,
      },
    }
  },
  computed: {
    ...mapState({ responsibles: (state) => state.responsibles }),
    showChat() {
      return this.headers.some((h) => h === 'new_messages_count')
    },
    activeHeaders() {
      const headers = [
        { text: 'ID', value: 'id' },
        { text: 'Fecha de registro', value: 'date_joined' },
        { text: 'Fecha firma', value: 'fecha_firma' },
        { text: 'Nombre/Razon social', value: 'fullname', sortable: false },
        { text: 'Tipo de agente', value: 'agent_type' },
        { text: 'Telefono', value: 'phone' },
        { text: 'Ultima entrada', value: 'last_login' },
        { text: 'Responsable', value: 'responsible_fn' },
        { text: 'Canal', value: 'canal_fn' },
        { text: 'Solicitud', value: 'bids_count', sortable: false },
        { text: 'Comisiones agente', value: 'paid_count' },
        { text: 'Comisiones canal', value: 'canal_paid_count' },
        { text: 'Estado', value: 'status' },
        { text: 'Doc', value: 'docs', sortable: false },
        { text: 'Scoring', value: 'scorings', sortable: false },
        { text: 'Llamadas', value: 'calls', sortable: false },
        { text: 'Estado de oferta', value: 'offer_status', sortable: false },
        { text: '', value: 'new_messages_count', sortable: false },
        { value: 'actions', sortable: false },
      ].filter((header) => this.headers.includes(header.value))

      if (this.role && this.role !== 'agent') {
        return headers.filter((h) => h.value !== 'agent_type')
      }
      return headers
    },
  },
  watch: {
    uploadToCallVisitDialog: {
      handler: async function (val) {
        if (!val) return
        if (!this.$store.state.cvusers.length) {
          try {
            await this.$store.dispatch('fetchCvUsers')
          } catch (e) {
            await this.$swal({
              title: 'Error',
              icon: 'error',
              text: 'No autorizado en Call&Visit. Ir al perfil',
            })
            this.uploadToCallVisitDialog = false
          }
        }
      },
    },
  },
  async created() {
    if (this.headers.some((header) => header.includes('responsible')) && !this.responsibles.length) {
      await this.$store.dispatch('fetchResponsibles')
    }
    if (this.role) this.query.role = this.role
  },
  methods: {
    async uploadToCallVisit() {
      this.loading = true
      try {
        await this.$axios.$post('/cv_integration/upload_cards/', {
          ...this.form,
          clients: this.selected.map((c) => c.id),
        })
        this.uploadToCallVisitDialog = false
      } catch (e) {
        await this.$swal({
          title: 'Error',
          icon: 'error',
          text: JSON.stringify(e.response.data),
        })
      } finally {
        this.loading = false
      }
    },
    onSelect({ item, items, value }) {
      if (!value) {
        if (item) {
          this.selected = this.selected.filter((selectedItem) => selectedItem.id !== item.id)
        } else {
          this.selected = []
        }
      } else {
        this.selected = item ? [...this.selected, item] : items
      }
      this.actionsSnackbar = this.selected.length > 0
    },
    async editResponsible() {
      await this.$axios.$patch(`users/manage_users/${this.reserved_userId}/`, {
        responsible: this.reserved_responsible || null,
      })
      await this.fetchUsers()
    },
    getDetailUrl(userId) {
      return `${this.detailUrl}/${userId}`
    },

    // other
    async fetchUsers() {
      try {
        this.loading = true
        if (
          String(this.query.page) !== String(this.$route.query.page) ||
          String(this.query.itemsPerPage) !== String(this.$route.query.itemsPerPage)
        ) {
          await this.$router.replace({
            query: Object.entries(this.query).reduce((a, [k, v]) => (v ? ((a[k] = v), a) : a), {}),
          })
        }
        const query = this.getQuery()
        const data = await this.$axios.$get(`${this.listUrl}/?${query}`)
        this.users = data.results
        this.total = data.count
      } catch (e) {
        if (e.response && e.response.status === 404 && this.query.page !== 1) {
          this.query.page = 1
          await this.fetchUsers()
        } else {
          console.error(e)
        }
      } finally {
        this.loading = false
      }
    },
    getQuery() {
      const query = constants.cleanEmpty({
        ...this.query,
        ordering:
          this.query.sortBy instanceof Array
            ? this.query.sortBy.map((sortBy, idx) => (this.query.sortDesc[idx] ? '+' : '-') + sortBy).join()
            : null,
        fields: this.headers.join(),
        role__isnull: this.role === 'null' ? true : null,
      })
      if (!query.statuses_in && this.statuses && this.statuses.length) query.statuses_in = this.statuses.join(',')
      return Object.keys(query)
        .filter((k) => query[k] !== null)
        .map((k) => {
          const value = query[k]
          return value instanceof Array ? `${k}=${value.join()}` : `${k}=${value}`
        })
        .join('&')
    },
    updateDateJoinedFilter(dates) {
      if (dates && dates.start && dates.end) {
        this.updateQuery({ date_joined__range: `${dates.start},${dates.end}` })
      } else {
        this.updateQuery({ date_joined__range: null })
      }
    },
    updateFechaFirmaFilter(dates) {
      if (dates && dates.start && dates.end) {
        this.updateQuery({ fecha_firma__range: `${dates.start},${dates.end}` })
      } else {
        this.updateQuery({ fecha_firma__range: null })
      }
    },
    async updateQuery(options) {
      this.query.page = 1
      Object.keys(options).forEach((key) => {
        const value = options[key]
        if (value) {
          this.query[key] = options[key]
        } else {
          delete this.query[key]
        }
      })
      const q = Object.entries(this.query).filter((entry) => {
        const value = entry[1]
        if (value instanceof Array) return value.length
        return !!value
      })
      await this.$router.replace({ query: q })
      await this.fetchUsers()
    },
    openChat(user) {
      this.$store.dispatch('chat/fetchParticipant', {
        participant: {
          id: user.id,
          name: user.fullname,
        },
        openChat: true,
      })
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
