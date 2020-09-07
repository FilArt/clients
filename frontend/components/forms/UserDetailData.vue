<template>
  <v-row class="flex-wrap">
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
        </v-row>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'UserDetailData',
  props: {
    user: {
      type: Object,
      default: () => {
        return {}
      },
    },
  },
  computed: {
    contactInfo() {
      const user = this.user
      return [
        {
          icon: 'mdi-account',
          text: 'Representante legal',
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
      const user = this.user

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
          value: user.last_modified,
        },
        {
          icon: 'mdi-account',
          text: 'Responsable',
          value: user.responsible,
        },
        {
          icon: 'mdi-target',
          text: 'Origin',
          value: user.affiliate,
        },
      ]
    },
  },
  methods: {
    async updateUser(field, value) {
      await this.$axios.$patch(`users/users/${this.user.id}/`, { [field]: value })
      await this.$swal({ title: 'Salvado', icon: 'success' })
    },
  },
}
</script>
