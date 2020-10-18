<template>
  <v-card class="pa-3">
    <snack-bar-it :noty-key="notificationKey" />

    <v-toolbar>
      <v-toolbar-title>
        {{ user.fullname }}
      </v-toolbar-title>
    </v-toolbar>

    <v-card-text>
      <v-row align="center">
        <v-col>
          <v-text-field
            v-model="settings.first_name"
            label="Nombre"
            :error-messages="errorMessages.first_name"
            :append-icon="user.first_name !== settings.first_name ? 'mdi-content-save' : null"
            @click:append="update({ first_name: settings.first_name })"
          />
          <v-text-field
            v-model="settings.last_name"
            label="Apellido"
            :error-messages="errorMessages.last_name"
            :append-icon="user.last_name !== settings.last_name ? 'mdi-content-save' : null"
            @click:append="update({ last_name: settings.last_name })"
          />
          <v-text-field
            v-model="settings.email"
            label="Email"
            :error-messages="errorMessages.email"
            :append-icon="user.email !== settings.email ? 'mdi-content-save' : null"
            @click:append="update({ email: settings.email })"
          />
          <v-select
            v-model="settings.role"
            label="Role"
            :error-messages="errorMessages.role"
            :items="[
              { text: 'Admin', value: 'admin' },
              { text: 'Agente', value: 'agent' },
              { text: 'Tramitacion', value: 'support' },
            ]"
            :append-icon="user.role !== settings.role ? 'mdi-content-save' : null"
            @click:append="update({ role: settings.role })"
          />

          <v-select
            v-if="user.role === 'agent'"
            v-model="settings.agent_type"
            label="Tipo de agente"
            :error-messages="errorMessages.agent_type"
            :items="[
              { text: 'Agente', value: 'agent' },
              { text: 'Canal', value: 'canal' },
            ]"
            :append-icon="user.agent_type !== settings.agent_type ? 'mdi-content-save' : null"
            @click:append="update({ agent_type: settings.agent_type })"
          />

          <agents-list
            v-if="settings.agent_type === 'canal'"
            v-model="settings.agents"
            label="Agentes de canal"
            multiple
            :error-messages="errorMessages.agents"
            :append-icon="JSON.stringify(user.agents) !== JSON.stringify(settings.agents) ? 'mdi-content-save' : ''"
            @click:append="update({ agents: settings.agents })"
          />

          <v-switch
            v-model="settings.fixed_salary"
            label="Sueldo fijo?"
            :error-messages="errorMessages.fixed_salary"
            :append-icon="user.fixed_salary !== settings.fixed_salary ? 'mdi-content-save' : null"
            @click:append="update({ fixed_salary: settings.fixed_salary })"
          />

          <v-select
            v-model="permissions"
            multiple
            label="Permisos"
            chips
            :items="[
              {
                text: 'Ofertas',
                value: 'offers',
              },
              {
                text: 'Comparador',
                value: 'calculator',
              },
              {
                text: 'Leeds - disponible',
                value: 'leeds_access',
              },
            ]"
            :append-icon="user.permissions !== settings.permissions ? 'mdi-content-save' : null"
            @click:append="update({ permissions: settings.permissions })"
          />
        </v-col>

        <v-divider vertical />

        <v-col>
          <v-btn block color="error" outlined @click="deleteUser">
            Eliminar usuario
            <v-icon right>mdi-trash-can-outline</v-icon>
          </v-btn>

          <br />

          <v-btn block color="indigo" outlined @click="changePassword">
            Cambiar contrasena
            <v-icon right>mdi-lock</v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </v-card-text>

    <v-card-text> </v-card-text>
  </v-card>
</template>

<script>
export default {
  components: {
    SnackBarIt: () => import('@/components/snackbar/SnackBarIt'),
    AgentsList: () => import('@/components/selects/AgentsList'),
  },
  async asyncData({ params, $axios }) {
    const user = await $axios.$get(`/users/manage_users/${params.id}/`)
    return {
      user,
      settings: { ...user },
      apiUrl: `users/manage_users/${user.id}/`,
    }
  },
  data() {
    return {
      notificationKey: 0,
      errorMessages: {},
    }
  },
  computed: {
    permissions: {
      set: function (val) {
        console.debug(val)
        this.settings.permissions = val
      },
      get: function () {
        return this.settings.permissions.map((p) => {
          return {
            text: p,
            value: p,
          }
        })
      },
    },
  },
  methods: {
    update(data) {
      this.errorMessages = {}
      this.$axios
        .$patch(this.apiUrl, data)
        .then((user) => {
          this.user = user
          this.settings = { ...user }
          this.notificationKey += 1
        })
        .catch((e) => (this.errorMessages = e.response.data))
    },
    deleteUser() {
      this.$swal({
        title: 'Eliminar usuario',
        icon: 'warning',
        buttons: true,
        dangerMode: true,
      }).then((isConfirmed) => {
        if (isConfirmed) {
          this.$axios
            .$delete(`users/manage_users/${this.user.id}`)
            .then(() => {
              this.$swal({ title: 'Listo', icon: 'success' }).then(() => {
                this.$router.back()
              })
            })
            .catch((e) => this.$swal({ title: 'Error', text: e.response.data }))
        }
      })
    },
    changePassword() {
      this.$swal({
        title: 'Puntar nuevo contrasena',
        content: 'input',
      }).then((password) => {
        this.$axios
          .$patch(`users/manage_users/${this.user.id}/`, { password })
          .then(() => {
            this.$swal({ title: 'Salvado', icon: 'success' })
          })
          .catch((e) => {
            this.$swal({
              title: 'Error',
              text: e.response.data.password.map((m, i) => `${i + 1}) ${m}`).join(' '),
              icon: 'error',
            })
          })
      })
    },
  },
}
</script>
