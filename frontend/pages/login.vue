<template>
  <v-container>
    <v-row class="text-center">
      <v-col>
        <v-card color="#004680">
          <g-g-logo />
        </v-card>
      </v-col>
    </v-row>

    <v-row id="flipCards">
      <v-col>
        <v-card v-show="showLogin" :loading="loading">
          <v-toolbar>
            <v-toolbar-title>Acceder</v-toolbar-title>
            <v-spacer />
            <v-toolbar-items>
              <v-btn small @click="flipCards"> Regístrate ahora. </v-btn>
            </v-toolbar-items>
          </v-toolbar>
          <v-form novalidate @submit.prevent="submit">
            <v-card-text>
              <v-alert v-if="error" type="error">
                {{ error }}
              </v-alert>
              <v-text-field
                v-model="form.email"
                prepend-icon="mdi-account"
                name="email"
                label="Email"
                type="text"
                @input="error = null"
              />
              <v-text-field
                id="password"
                v-model="form.password"
                prepend-icon="mdi-lock"
                name="password"
                label="Сontraseña"
                type="password"
                autocomplete="current-password"
              />
            </v-card-text>
            <v-card-actions>
              <v-row>
                <v-col>
                  <v-btn block type="submit" dark color="#004680" :loading="loading">
                    Acceder
                    <v-icon color="#004680" right> mdi-logout </v-icon>
                  </v-btn>
                </v-col>
                <v-col class="flex-grow-0">
                  <v-btn :loading="loading" outlined rounded @click="passwordForgotten">
                    ¿Olvidasde la contraseña?
                    <v-icon right> mdi-lock-reset </v-icon>
                  </v-btn>
                </v-col>
              </v-row>
            </v-card-actions>
          </v-form>
        </v-card>

        <v-card v-show="!showLogin" :loading="loading">
          <v-toolbar>
            <v-toolbar-title>Registrarse</v-toolbar-title>
            <v-spacer />
            <v-toolbar-items>
              <v-btn small @click="flipCards"> Accede a tu cuenta </v-btn>
            </v-toolbar-items>
          </v-toolbar>
          <v-form novalidate @submit.prevent="submitRegister">
            <v-card-text>
              <v-text-field
                v-model="form.email"
                prepend-icon="mdi-account"
                name="email"
                label="Email"
                type="text"
                :error-messages="errorMessages2.email"
                @input="errorMessages2.email = null"
              />
              <v-text-field
                id="new-password"
                v-model="form.password"
                prepend-icon="mdi-lock"
                name="password"
                label="Сontraseña"
                type="password"
                autocomplete="new-password"
              />
            </v-card-text>
            <v-card-actions>
              <v-btn type="submit" color="#004680" block :loading="loading" :disabled="!$store.state.privacyAccepted">
                Registrarse
                <v-icon right> mdi-account-plus </v-icon>
              </v-btn>
            </v-card-actions>
            <v-card-actions>
              <privacy />
            </v-card-actions>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  auth: 'guest',
  components: { GGLogo: () => import('~/components/GGLogo'), Privacy: () => import('~/components/other/Privacy') },
  data: () => ({
    loading: false,
    showLogin: true,

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
        .animate([{ transform: 'rotateX(180grad)' }, { transform: 'rotateX(0deg)' }], { duration: 500 })
    },
    async submit() {
      if (!this.form.email || !this.form.email.length) {
        this.error = 'Ingrese su Email'
        return
      }
      this.loading = true
      this.error = null
      try {
        await this.$auth.loginWith('local', { data: this.form })

        const { user } = this.$auth
        const { role } = user

        if (role === null) {
          await this.$router.push('/ofertas')

          // load chat messages
          // TODO: move it to Chat.vue
          this.$store.dispatch('chat/fetchParticipant')

          if (!user.phone) {
            await this.$swal({
              title: 'Por favor, complete su perfil por completo.',
              text:
                'Su perfil completo nos ayudará a conocernos mejor, y nos permitirá proporcionarle un soporte más completo y ampliado.',
              icon: 'warning',
            })
            await this.$router.push('/profile')
          }
        } else {
          const path = role === 'admin' ? '/admin/dashboard' : '/agente/clientes'
          await this.$router.push(path)
        }
      } catch (e) {
        console.log(e)
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

      const willDelete = await this.$swal({
        title: '¿Estás seguro de que deseas restablecer tu contraseña?',
        icon: 'warning',
        buttons: true,
        dangerMode: true,
      })

      if (!willDelete) return

      try {
        await this.$axios.post('users/register_user/reset_password/', this.form)
      } catch (e) {
        this.error = e.response.data
      }

      await this.$swal({
        title: 'Сorreo electrónico con una nueva contraseña ha sido enviado a su correo.',
        icon: 'success',
      })
    },
  },
}
</script>
