<template>
  <div>
    <v-row class="text-center">
      <v-col>
        <g-g-logo />
      </v-col>
    </v-row>
    <v-row class="flex-wrap">
      <v-col>
        <v-card>
          <v-toolbar>
            <v-toolbar-title>Acceder</v-toolbar-title>
          </v-toolbar>
          <v-form @submit.prevent="submit" novalidate>
            <v-card-text>
              <v-alert v-if="error" type="error">{{ error }}</v-alert>
              <v-text-field
                prepend-icon="mdi-account"
                name="email"
                label="Email"
                type="text"
                v-model="form.email"
                @input="error = null"
              ></v-text-field>
              <v-text-field
                id="password"
                prepend-icon="mdi-lock"
                name="password"
                label="Сontraseña"
                type="password"
                v-model="form.password"
              ></v-text-field>
            </v-card-text>
            <v-card-actions>
              <v-btn block type="submit" color="primary"
                >Acceder
                <v-icon right>mdi-logout</v-icon>
              </v-btn>
            </v-card-actions>
            <v-card-actions>
              <v-btn block color="warning" @click="passwordForgotten">
                ¿Olvidasde la contraseña?
              </v-btn>
            </v-card-actions>
          </v-form>
        </v-card>
      </v-col>
      <v-col>
        <v-card>
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
                @input="errorMessages2.email = null"
              ></v-text-field>
            </v-card-text>
            <v-card-actions>
              <v-btn
                type="submit"
                color="primary"
                block
                :disabled="!privacyAccepted"
                >Registrarse
                <v-icon right>mdi-account-plus</v-icon>
              </v-btn>
            </v-card-actions>
            <v-card-actions>
              <v-checkbox
                :success="privacyAccepted"
                :error="!privacyAccepted"
                v-model="privacyAccepted"
                persistent-hint
                hint="Sus datos personales se utilizarán para simplificar su trabajo con el sitio, controlar el acceso a su cuenta y para otros fines descritos en nuestra política de privacidad."
                label="Estoy de acuerdo"
              />
            </v-card-actions>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import GGLogo from '~/components/GGLogo'
export default {
  components: { GGLogo },
  middleware: 'auth',
  data: () => ({
    privacyAccepted: false,
    error: null,
    errorMessages2: { email: null },
    form: {
      email: null,
      password: null
    }
  }),
  methods: {
    async submit() {
      if (!this.form.email || !this.form.email.length) {
        this.error = 'Ingrese su Email'
        return
      }

      this.error = null
      try {
        const response = await this.$auth.login({ data: this.form })
        this.$auth.setRefreshToken('local', response.data.refresh)
      } catch (e) {
        const errorMsg = e.response.data.detail
        if (errorMsg === 'No active account found with the given credentials') {
          this.error = 'La cuenta no existe'
        } else {
          this.error = 'Autorización fallida'
        }
      }
    },
    async submitRegister() {
      if (!this.form.email || !this.form.email.length) {
        this.errorMessages2.email = ['Ingrese su Email']
        return
      }
      this.errorMessages2 = { email: null }
      try {
        await this.$axios.post('users/register_user/', this.form)
      } catch (e) {
        this.errorMessages2 = e.response.data
      }
    },
    passwordForgotten() {
      if (!this.form.email || !this.form.email.length) {
        this.error = 'Ingrese su Email'
        return
      }
      this.$axios
        .post('users/register_user/reset_password/', this.form)
        .then(() =>
          this.$swal({
            title:
              'Сorreo electrónico con una nueva contraseña ha sido enviado a su correo.',
            icon: 'success'
          })
        )
        .catch(e => (this.error = e.response.data))
    }
  }
}
</script>
