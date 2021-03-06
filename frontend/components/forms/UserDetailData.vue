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
          <v-text-field
            v-for="date in datesInfo"
            :key="date.text"
            v-model="date.value"
            :prepend-icon="date.icon"
            :label="date.text"
            :append-icon="readonly ? null : 'mdi-content-save'"
            :readonly="readonly"
            dense
            @click:append="updateUser(date.field, date.value.includes('/') ? date.value : unformatDate(date.value))"
          />

          <!--        <v-select-->
          <!--          v-model="source"-->
          <!--          dense-->
          <!--          prepend-icon="mdi-target"-->
          <!--          label="Origin"-->
          <!--          :items="[-->
          <!--            {-->
          <!--              text: 'Online',-->
          <!--              value: 'default',-->
          <!--            },-->
          <!--            {-->
          <!--              text: 'Call&Visit',-->
          <!--              value: 'call_n_visit',-->
          <!--            },-->
          <!--          ]"-->
          <!--          :readonly="readonly"-->
          <!--          :append-icon="source !== user.source ? 'mdi-content-save' : null"-->
          <!--          @click:append="updateUser('source', source)"-->
          <!--        />-->

          <v-autocomplete
            v-model="responsible"
            dense
            :readonly="readonly"
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
          v-model="user.observations"
          label="Observaciones"
          dense
          prepend-icon="mdi-eye"
          :append-icon="readonly ? null : 'mdi-content-save'"
          @click:append="updateUser('observations', user.observations)"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState } from 'vuex'
import { format, parseISO, parse } from 'date-fns'
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
      user: {},
      responsible: null,
      source: null,
      phone: null,
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
          value: user.phone_city,
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
      ]
    },
    datesInfo() {
      const { user } = this
      return [
        {
          icon: 'mdi-calendar',
          text: 'Ultima entrada',
          field: 'last_login',
          value: this.formatDate(user.last_login),
        },
        {
          icon: 'mdi-calendar',
          text: 'Fecha de registro',
          field: 'date_joined',
          value: this.formatDate(user.date_joined),
        },
        {
          icon: 'mdi-calendar',
          text: 'Fecha firma',
          field: 'fecha_firma',
          value: this.formatDate(user.fecha_firma),
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
      'date_joined',
      'last_login',
      'email',
      'legal_representative',
      'last_modified',
      'fecha_firma',
      'company_name',
      'cif_nif',
    ]
    const user = await this.$axios.$get(`users/users/${this.userId}/?fields=${fields}`)
    this.user = user
    this.responsible = user.responsible
    this.source = user.source

    if (!this.responsibles.length) {
      await this.$store.dispatch('fetchResponsibles')
    }
  },
  methods: {
    unformatDate(maybeDate) {
      return maybeDate ? parse(maybeDate, DATE_FORMAT, new Date()).toISOString() : null
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
        const user = await this.$axios.$patch(`users/users/${this.userId}/`, { [field]: value })
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
