<template>
  <div>
    <v-menu v-if="!$auth.loggedIn" v-model="menu" :close-on-content-click="false" :nudge-width="200" offset-x>
      <template v-slot:activator="{ on }">
        <v-btn color="indigo" dark v-on="on"> Login </v-btn>
      </template>

      <v-card>
        <v-card-text>
          <v-form @submit.prevent="login">
            <email-field v-model="email" />
            <v-text-field
              id="password"
              v-model="password"
              prepend-icon="mdi-lock"
              name="password"
              label="Сontraseña"
              type="password"
              autocomplete="current-password"
            />
            <submit-button />
          </v-form>
        </v-card-text>
      </v-card>
    </v-menu>
    <calculator detail-url="/calc/place_for_id?nosupport" />
  </div>
</template>

<script>
import Calculator from '@/components/forms/Calculator'
import EmailField from '@/components/fields/emailField'
import SubmitButton from '@/components/buttons/submitButton'
export default {
  layout: 'empty',
  components: { SubmitButton, EmailField, Calculator },
  auth: false,
  data() {
    return {
      menu: false,
      email: null,
      password: null,
    }
  },
  methods: {
    async login() {
      await this.$auth.loginWith('local', { data: { email: this.email, password: this.password } })
      await this.$router.push('/calc')
      this.menu = false
    },
  },
}
</script>
