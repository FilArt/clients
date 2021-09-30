<template>
  <v-container>
    <v-row justify="space-around">
      <v-col cols="12" lg="5" class="pa-0 ma-0">
        <v-toolbar short dense>
          <v-spacer />
          <v-toolbar-title>Datos de contacto</v-toolbar-title>
          <v-spacer />
        </v-toolbar>
        <v-card-text class="d-flex flex-row flex-wrap">
          <v-text-field
            v-for="(item, idx) in contactInfo"
            :key="idx"
            v-model="contactInfo[idx].value"
            dense
            :prepend-icon="item.icon"
            :label="item.text"
            :append-icon="readonly ? null : item.field ? 'mdi-content-save' : ''"
            @click:append="updateUser(item.field, contactInfo[idx].value)"
          />
        </v-card-text>
      </v-col>

      <v-col cols="12" lg="5" class="pa-0 ma-0">
        <v-toolbar short dense>
          <v-spacer />
          <v-toolbar-title> Otro </v-toolbar-title>
          <v-spacer />
        </v-toolbar>
        <v-card-text class="d-flex flex-row flex-wrap">
          <v-dialog v-for="(date, idx) in datesInfo" :key="date.text" v-model="dialogs[idx]" max-width="600px">
            <template v-slot:activator="{ on }">
              <v-text-field
                v-model="date.value"
                :prepend-icon="date.icon"
                :label="date.text"
                :append-icon="!date.editable ? null : 'mdi-content-save'"
                :readonly="!date.editable"
                dense
                v-on="on"
              />
            </template>
            <v-card>
              <v-card-text>
                <v-row>
                  <v-col>
                    <date-time-filter v-model="date.value" format="DD/MM/YYYY HH:mm" inline />
                  </v-col>
                </v-row>
                <v-row>
                  <v-col class="flex-grow-0">
                    <v-btn color="warning" @click="dialogs[idx] = false"> Cancellar </v-btn>
                  </v-col>
                  <v-col>
                    <v-btn
                      block
                      color="info"
                      @click="
                        updateUser(date.field, date.value)
                        dialogs[idx] = false
                      "
                    >
                      Salvar
                    </v-btn>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-dialog>

          <v-autocomplete
            v-model="responsible"
            dense
            prepend-icon="mdi-account"
            label="Responsable"
            item-text="fullname"
            item-value="id"
            :items="responsibles"
            :append-icon="responsible !== user.responsible ? 'mdi-content-save' : null"
            @click:append="updateUser('responsible', responsible)"
          />
        </v-card-text>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-textarea
          v-model="user['observations']"
          label="Observaciones"
          dense
          prepend-icon="mdi-eye"
          :append-icon="readonly ? null : 'mdi-content-save'"
          @click:append="updateUser('observations', user['observations'])"
        />
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
  components: { DateTimeFilter: () => import('@/components/DateTimeFilter') },
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
      user: {},
      responsible: null,
      source: null,
      phone: null,
      dialogs: {},
    }
  },
  computed: {
    ...mapState({ responsibles: (state) => state.responsibles }),
    contactInfo() {
      const { user } = this
      return [
        {
          icon: 'mdi-person',
          text: 'Nombre',
          value: user.company_name,
          field: 'company_name',
        },
        {
          icon: 'mdi-account',
          text: 'Persona de contacto',
          value: user.legal_representative,
          field: 'legal_representative',
        },
        {
          icon: 'mdi-phone',
          text: 'Telefono',
          value: user.phone,
          field: 'phone',
        },
        {
          icon: 'mdi-phone',
          text: 'Telefono fijo',
          value: user['phone_city'],
          field: 'phone_city',
        },
        {
          icon: 'mdi-email',
          text: 'Email',
          value: user.email,
          field: 'email',
        },
        {
          text: 'CIF/NIF',
          field: 'cif_nif',
          value: user.cif_nif,
        },
        {
          text: 'Call-Visit ID',
          field: 'call_visit_id',
          value: user.call_visit_id,
        },
      ]
    },
    datesInfo() {
      const { user } = this
      return [
        {
          icon: 'mdi-calendar',
          text: 'Ultimo cambio',
          field: 'last_modified',
          value: this.formatDate(user['last_modified']),
          editable: false,
        },
        {
          icon: 'mdi-calendar',
          text: 'Fecha de registro',
          field: 'created_at',
          value: this.formatDate(user['created_at']),
          editable: false,
        },
        {
          icon: 'mdi-calendar',
          text: 'Fecha firma',
          field: 'fecha_firma',
          value: this.formatDate(user['fecha_firma']),
          editable: false,
        },
      ]
    },
  },
  async created() {
    const fields = [
      'observations',
      'source',
      'responsible',
      'phone',
      'phone_city',
      'created_at',
      'email',
      'legal_representative',
      'last_modified',
      'fecha_firma',
      'company_name',
      'cif_nif',
      'call_visit_id',
    ]
    const user = await this.$axios.$get(`users/users/${this.userId}/?fields=${fields}`)
    this.user = user
    this.responsible = user.responsible
    this.source = user.source

    if (!this.responsibles.length) {
      const isAgent = this.$auth.user && this.$auth.user.role === 'agent'
      await this.$store.dispatch('fetchResponsibles', isAgent)
    }
  },
  methods: {
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
        const user = await this.$axios.$patch(`users/users/${this.userId}/`, { [field]: value })
        this.user = user
        this.$toast.global.done()
        this.$emit('user-updated', user)
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
