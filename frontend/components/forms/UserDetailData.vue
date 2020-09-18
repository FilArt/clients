<template>
  <v-row class="flex-wrap">
    <snack-bar-it :noty-key="notificationKey" />

    <v-col md="6" cols="12">
      <v-toolbar elevation="10" short dense>
        <v-spacer />
        <v-toolbar-title>Datos de contacto</v-toolbar-title>
        <v-spacer />
      </v-toolbar>
      <v-card elevation="10" class="pa-3">
        <v-row>
          <v-col v-for="(item, idx) in contactInfo" :key="idx" xl="4" md="6" cols="12">
            <v-text-field
              v-model="contactInfo[idx].value"
              :prepend-icon="item.icon"
              :label="item.text"
              filled
              :append-icon="item.field ? 'mdi-content-save' : ''"
              @click:append="updateUser(item.field, contactInfo[idx].value)"
            />
          </v-col>
        </v-row>
      </v-card>
    </v-col>

    <v-col>
      <v-toolbar short dense elevation="10">
        <v-spacer />
        <v-toolbar-title> Otro </v-toolbar-title>
        <v-spacer />
      </v-toolbar>
      <v-card elevation="10" class="pa-3">
        <v-row class="flex-wrap">
          <v-col v-for="date in datesInfo" :key="date.text" xl="4" md="6" cols="12">
            <v-text-field :prepend-icon="date.icon" :label="date.text" :value="date.value" outlined shaped />
          </v-col>

          <v-col xl="4" md="6" cols="12">
            <v-select
              v-model="source"
              prepend-icon="mdi-target"
              label="Origin"
              outlined
              shaped
              :items="[
                {
                  text: 'Online',
                  value: 'default',
                },
                {
                  text: 'Call&Visit',
                  value: 'call_n_visit',
                },
              ]"
              :append-icon="source !== user.source ? 'mdi-content-save' : null"
              @click:append="updateUser('source', source)"
            />
          </v-col>

          <v-col xl="4" md="6" cols="12">
            <v-autocomplete
              v-model="responsible"
              prepend-icon="mdi-account"
              label="Responsable"
              item-text="fullname"
              item-value="id"
              outlined
              shaped
              :items="responsibles"
              :append-icon="responsible !== user.responsible ? 'mdi-content-save' : null"
              @click:append="updateUser('responsible', responsible)"
            />
          </v-col>
        </v-row>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import { mapState } from 'vuex'
export default {
  name: 'UserDetailData',
  components: {
    SnackBarIt: () => import('@/components/snackbar/SnackBarIt'),
  },
  props: {
    userId: {
      type: [Number, String],
      default: 0,
    },
  },
  data() {
    return {
      user: { phones: [] },
      responsible: null,
      source: null,
      notificationKey: 0,
    }
  },
  computed: {
    ...mapState({ responsibles: (state) => state.responsibles }),
    contactInfo() {
      const { user } = this

      return [
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
        ...user.phones
          .filter((n) => n)
          .map((phone) => {
            return {
              icon: 'mdi-phone',
              text: 'Telefono',
              value: phone.number,
              field: 'phone',
            }
          }),
        {
          icon: 'mdi-email',
          text: 'Email',
          value: user.email,
          field: 'email',
        },
      ]
    },
    datesInfo() {
      const { user } = this
      return [
        {
          icon: 'mdi-calendar',
          text: 'Ultima entrada',
          value: user.last_login,
        },
        {
          icon: 'mdi-calendar',
          text: 'Fecha de registro',
          value: user.date_joined,
        },
        {
          icon: 'mdi-calendar',
          text: 'Fecha firma',
          value: user.fecha_firma,
        },
      ]
    },
  },
  async created() {
    const fields = [
      'phones',
      'source',
      'responsible',
      'phone',
      'date_joined',
      'last_login',
      'email',
      'legal_representative',
      'last_modified',
      'fecha_firma',
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
    notify() {
      this.notificationKey += 1
    },
    async updateUser(field, value) {
      const user = await this.$axios.$patch(`users/users/${this.userId}/`, { [field]: value })
      this.notify()
      this.$emit('user-updated', user)
    },
  },
}
</script>
