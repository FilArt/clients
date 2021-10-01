<template>
  <v-container>
    <v-row justify="space-around">
      <v-col>
        <v-toolbar short dense>
          <v-spacer />
          <v-toolbar-title>Datos de contacto</v-toolbar-title>
          <v-spacer />
        </v-toolbar>
        <v-card-text>
          <v-card-text class="flex-wrap">
            <v-flex v-for="(item, idx) in userFields" :key="idx">
              <v-text-field
                v-model="changedUser[item.field]"
                dense
                :prepend-icon="item.icon"
                :label="item.text"
                :append-icon="!readonly && changedUser[item.field] !== user[item.field] ? 'mdi-content-save' : null"
                @click:append="updateUser(item.field, changedUser[item.field])"
              />
            </v-flex>

            <v-flex>
              <v-autocomplete
                v-model="responsible"
                dense
                prepend-icon="mdi-account-tie"
                label="Responsable"
                item-text="fullname"
                item-value="id"
                :items="responsibles"
                :append-icon="responsible !== user.responsible ? 'mdi-content-save' : null"
                @click:append="updateUser('responsible', responsible)"
              />
            </v-flex>
          </v-card-text>
        </v-card-text>
      </v-col>

      <v-col>
        <v-toolbar short dense>
          <v-spacer />
          <v-toolbar-title>Cambias</v-toolbar-title>
          <v-spacer />
        </v-toolbar>
        <v-card-text class="flex-wrap">
          <v-row>
            <v-col>
              <v-list id="commentsList" style="overflow-y: scroll; height: 400px">
                <template v-for="item in userHistory">
                  <v-list-item :key="item.id">
                    <v-list-item-content>
                      <v-list-item-title>
                        <v-row>
                          <v-col>
                            <caption style="color: green">
                              {{
                                formatDate(item.requested_at)
                              }}
                            </caption>
                          </v-col>
                          <v-spacer />
                          <v-col>
                            <nuxt-link :to="'/admin/usuarios/' + item.user">{{ item.fullname }}</nuxt-link>
                          </v-col>
                        </v-row>
                      </v-list-item-title>

                      <pre>{{ item.data }}</pre>
                    </v-list-item-content>
                  </v-list-item>

                  <v-divider :key="'d' + item.id" />
                </template>
              </v-list>

              <v-text-field
                v-model="comment"
                label="Nuevo comentario"
                append-icon="mdi-send"
                @keyup.enter="
                  updateUser('observations', comment)
                  comment = ''
                "
                @click:append="
                  updateUser('observations', comment)
                  comment = ''
                "
              />
            </v-col>
          </v-row>
        </v-card-text>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState } from 'vuex'
import { format, parseISO } from 'date-fns'
const DATE_FORMAT = 'dd/MM/yyyy HH:mm'
export default {
  name: 'UserDetailData',
  props: {
    userId: {
      type: [Number, String],
      default: 0,
    },
    readonly: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      comment: '',
      user: {},
      userHistory: [],
      responsible: null,
      source: null,
      phone: null,
      dialogs: {},
      changedUser: {},
      userFields: [
        {
          icon: 'mdi-domain',
          text: 'Nombre',
          field: 'company_name',
        },
        {
          icon: 'mdi-account',
          text: 'Persona de contacto',
          field: 'legal_representative',
        },
        {
          icon: 'mdi-counter',
          text: 'CIF/NIF',
          field: 'cif_nif',
        },
        {
          icon: 'mdi-phone',
          text: 'Telefono',
          field: 'phone',
        },
        {
          icon: 'mdi-deskphone',
          text: 'Telefono fijo',
          field: 'phone_city',
        },
        {
          icon: 'mdi-email',
          text: 'Email',
          field: 'email',
        },
        {
          icon: 'mdi-calendar',
          text: 'Ultimo cambio',
          field: 'last_modified',
          readonly: true,
        },
        {
          icon: 'mdi-calendar-plus',
          text: 'Fecha de registro',
          field: 'created_at',
          readonly: true,
        },
        {
          icon: 'mdi-calendar-check',
          text: 'Fecha firma',
          field: 'fecha_firma',
          readonly: true,
        },
      ],
    }
  },
  computed: {
    ...mapState({ responsibles: (state) => state.responsibles }),
  },
  async mounted() {
    await this.refresh()
    if (!this.responsibles.length) {
      const isAgent = this.$auth.user && this.$auth.user.role === 'agent'
      await this.$store.dispatch('fetchResponsibles', isAgent)
    }
  },
  methods: {
    async refresh() {
      const fields = this.userFields.map((f) => f.field).join()
      const user = await this.$axios.$get(`users/users/${this.userId}/?fields=${fields}`)
      this.user = user
      this.changedUser = { ...user }
      this.responsible = user.responsible
      this.source = user.source
      await this.getUserHistory()
    },
    async getUserHistory() {
      this.userHistory = await this.$axios.$get(`/users/manage_users/${this.userId}/history/`)
      const self = this
      setTimeout(function () {
        const cl = self.$el.querySelector('#commentsList')
        cl.scrollTop = cl.scrollHeight
      }, 250)
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
    formatDate(dt) {
      if (!dt || dt.includes('/')) return dt
      try {
        return format(parseISO(dt), DATE_FORMAT)
      } catch (e) {
        return null
      }
    },
    async updateUser(field, value) {
      try {
        await this.$axios.$patch(`users/users/${this.userId}/`, { [field]: value })
        await this.refresh()
        this.$toast.global.done()
        this.$emit('user-updated', { ...this.user })
        this.getUserHistory()
      } catch (e1) {
        try {
          const errText = e1.response.data[field][0]
          await this.$swal({ title: 'Error', text: errText, icon: 'error' })
        } catch (e2) {
          console.log(e2)
        }
      }
    },
  },
}
</script>
