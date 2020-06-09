<template>
  <v-flex>
    <v-card class="elevation-12">
      <v-row>
        <v-col>
          <v-toolbar dark color="primary">
            <v-toolbar-title>Login</v-toolbar-title>
          </v-toolbar>
          <v-form @submit.prevent="submit" novalidate>
            <v-card-text>
              <p class="error" v-if="error">{{ error }}</p>
              <v-text-field
                prepend-icon="mdi-account"
                name="email"
                label="Email"
                type="text"
                v-model="form.email"
              ></v-text-field>
              <v-text-field
                id="password"
                prepend-icon="mdi-lock"
                name="password"
                label="Password"
                type="password"
                v-model="form.password"
              ></v-text-field>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn type="submit" color="primary">Login</v-btn>
            </v-card-actions>
          </v-form>
        </v-col>
        <v-col>
          <v-toolbar>
            <v-toolbar-title>Registrarse</v-toolbar-title>
          </v-toolbar>
          <v-form @submit.prevent="submitRegister" novalidate>
            <v-card-text>
              <v-text-field
                prepend-icon="mdi-account"
                name="email"
                label="Email"
                type="text"
                :error-messages="errorMessages2.email"
                v-model="form.email"
              ></v-text-field>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn type="submit" color="primary">Registrarse</v-btn>
            </v-card-actions>
          </v-form>
        </v-col>
      </v-row>
    </v-card>
  </v-flex>
</template>

<script>
export default {
  middleware: 'auth',
  data: () => ({
    error: null,
    errorMessages2: { email: null },
    form: {
      email: '',
      password: ''
    }
  }),
  methods: {
    async submit() {
      this.error = null
      try {
        const response = await this.$auth.login({ data: this.form })
        this.$auth.setRefreshToken('local', response.data.refresh)
      } catch (e) {
        this.error = 'Login failed.'
      }
    },
    async submitRegister() {
      this.errorMessages2 = { email: null }
      try {
        await this.$axios.post('users/register_user/', this.form)
      } catch (e) {
        this.errorMessages2 = e.response.data
      }
    }
  }
}
</script>
