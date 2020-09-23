<template>
  <v-row justify="space-around">
    <snack-bar-it :noty-key="notificationKey" />

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
          :append-icon="item.field ? 'mdi-content-save' : ''"
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
          dense
          :prepend-icon="date.icon"
          :label="date.text"
          :value="date.value"
        />

        <v-select
          v-model="source"
          dense
          prepend-icon="mdi-target"
          label="Origin"
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
