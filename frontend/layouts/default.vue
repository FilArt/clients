<template>
  <v-app>
    <v-navigation-drawer
      v-if="$auth.loggedIn"
      v-model="drawer"
      fixed
      app
      clipped
    >
      <v-list>
        <v-list-item
          v-for="(item, i) in items"
          :key="i"
          :to="item.to"
          router
          exact
        >
          <v-list-item-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar fixed app v-if="$auth.loggedIn" clipped-left>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-toolbar-title v-text="title" />
      <v-spacer />
      <theme-switcher />
      <v-btn v-if="$auth" icon @click.stop="$auth.logout">
        <v-icon>mdi-logout</v-icon>
      </v-btn>
    </v-app-bar>
    <v-content>
      <v-container>
        <nuxt />
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import ThemeSwitcher from '~/components/ThemeSwitcher'
export default {
  name: 'Default',
  components: { ThemeSwitcher },
  data() {
    return {
      refreshTokenIntervalId: null,
      drawer: true,
      items: [
        {
          icon: 'mdi-account',
          title: 'Perfil',
          to: '/profile',
        },
        {
          icon: 'mdi-briefcase',
          title: 'Cartera',
          to: '/bids',
        },

        {
          icon: 'mdi-calculator',
          title: 'Comparador',
          to: '/calculator',
        },
        {
          icon: 'mdi-offer',
          title: 'Ofertas',
          to: '/offers',
        },
      ],
      title: 'Gestion Group',
    }
  },
  async mounted() {
    await this.refreshToken()
    if (this.refreshTokenIntervalId) {
      clearInterval(this.refreshTokenIntervalId)
    }
    this.refreshTokenIntervalId = setInterval(this.refreshToken, 1000 * 60) // refresh minute
  },
  methods: {
    async refreshToken() {
      if (!this.$auth.loggedIn) return
      const refreshToken = this.$auth.getRefreshToken('local')
      if (!refreshToken) return
      try {
        const responseData = await this.$axios.$post('users/refresh', {
          refresh: refreshToken,
        })
        await this.$auth.setToken('local', 'Bearer ' + responseData.access)
      } catch (e) {
        await this.$auth.logout()
      }
    },
  },
}
</script>
