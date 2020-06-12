<template>
  <div>
    <v-row class="text-center">
      <v-col>
        <g-g-logo />
      </v-col>
    </v-row>

    <div id="flipCards">
      <v-card v-show="showLogin" :loading="loading">
        <v-toolbar>
          <v-toolbar-title>Acceder</v-toolbar-title>
          <v-spacer />
          <v-toolbar-items>
            <v-btn small @click="flipCards">Regístrate ahora.</v-btn>
          </v-toolbar-items>
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
            <v-btn block type="submit" color="primary" :loading="loading"
              >Acceder
              <v-icon right>mdi-logout</v-icon>
            </v-btn>
          </v-card-actions>
          <v-card-actions>
            <v-btn
              block
              :loading="loading"
              @click="passwordForgotten"
              outlined
              rounded
            >
              ¿Olvidasde la contraseña?
              <v-icon right>mdi-lock-reset</v-icon>
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card>

      <v-card v-show="!showLogin" :loading="loading">
        <v-toolbar>
          <v-toolbar-title>Registrarse</v-toolbar-title>
          <v-spacer />
          <v-toolbar-items>
            <v-btn small @click="flipCards">Accede a tu cuenta</v-btn>
          </v-toolbar-items>
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
              :loading="loading"
              :disabled="!privacyAccepted"
              >Registrarse
              <v-icon right>mdi-account-plus</v-icon>
            </v-btn>
          </v-card-actions>
          <v-card-actions>
            <v-checkbox
              v-model="privacyAccepted"
              :success="privacyAccepted"
              :error="!privacyAccepted"
              :hint="privacyHint + ' política de privacidad.'"
              label="Estoy de acuerdo"
              persistent-hint
            >
              <template v-slot:message>
                {{ privacyHint }}
                <a target="_blank" href="https://gestiongroup.es/privacy_policy"
                  >política de privacidad.</a
                >
              </template>
            </v-checkbox>
          </v-card-actions>
        </v-form>
      </v-card>
    </div>
  </div>
</template>

<script>
import GGLogo from '~/components/GGLogo'
export default {
  components: { GGLogo },
  data: () => ({
    loading: false,
    showLogin: true,
    privacyAccepted: false,
    privacyHint:
      'Sus datos personales se utilizarán para simplificar su trabajo con el sitio, controlar el acceso a su cuenta y para otros fines descritos en nuestra',

    error: null,
    errorMessages2: { email: null },
    form: {
      email: null,
      password: null,
    },
  }),
  methods: {
    async flipCards() {
      this.showLogin = !this.showLogin
      document
        .getElementById('flipCards')
        .animate(
          [{ transform: 'rotateX(180grad)' }, { transform: 'rotateX(0deg)' }],
          { duration: 500 }
        )
    },
    async submit() {
      if (!this.form.email || !this.form.email.length) {
        this.error = 'Ingrese su Email'
        return
      }
      this.loading = true
      this.error = null
      try {
        const response = await this.$auth.login({ data: this.form })
        this.$auth.setRefreshToken('local', response.data.refresh)
        this.$auth.user.permissions.offers
          ? await this.$router.push('/offers')
          : await this.$router.push('/bids')
      } catch (e) {
        const errorMsg = e.response.data.detail
        if (errorMsg === 'No active account found with the given credentials') {
          this.error = 'La cuenta no existe'
        } else {
          this.error = 'Autorización fallida'
        }
      } finally {
        this.loading = false
      }
    },
    async submitRegister() {
      if (!this.form.email || !this.form.email.length) {
        this.errorMessages2.email = ['Ingrese su Email']
        return
      }
      this.loading = true
      this.errorMessages2 = { email: null }
      try {
        await this.$axios.post('users/register_user/', this.form)
        await this.$swal({
          title: 'Registrado!',
          icon: 'success',
        })
        await this.flipCards()
      } catch (e) {
        this.errorMessages2 = e.response.data
      } finally {
        this.loading = false
      }
    },
    async passwordForgotten() {
      if (!this.form.email || !this.form.email.length) {
        this.error = 'Ingrese su Email'
        return
      }
      this.loading = true
      try {
        await this.$axios.post('users/register_user/reset_password/', this.form)
        await this.$swal({
          title:
            'Сorreo electrónico con una nueva contraseña ha sido enviado a su correo.',
          icon: 'success',
        })
      } catch (e) {
        this.error = e.response.data
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
