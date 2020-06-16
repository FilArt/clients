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
      <nuxt />
    </v-content>
  </v-app>
</template>

<script>
export default {
  name: 'Default',
  components: { ThemeSwitcher: () => import('~/components/ThemeSwitcher') },
  data() {
    return {
      refreshTokenIntervalId: null,
      drawer: true,
      title: 'Gestion Group',
    }
  },
  computed: {
    items() {
      const items = [
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
      ]
      if (this.$auth.user.permissions.includes('calculator')) {
        items.push({
          icon: 'mdi-calculator',
          title: 'Comparador',
          to: '/calculator',
        })
      }
      if (this.$auth.user.permissions.includes('offers')) {
        items.push({
          icon: 'mdi-offer',
          title: 'Ofertas',
          to: '/offers',
        })
      }
      const role = this.$auth.user.role
      if (role) {
        items.push({
          icon: role === 'support' ? 'mdi-lifebuoy' : '',
          title: role === 'support' ? 'Support' : '',
          to: role,
        })
      }
      return items
    },
  },
  async mounted() {
    await this.refreshToken()
    this.$store.state.refreshTokenIds.forEach((token) => {
      clearInterval(token)
    })
    const refreshTokenIntervalId = setInterval(this.refreshToken, 1000 * 60)
    this.$store.commit('addRefreshTokenId', refreshTokenIntervalId)
  },
  methods: {
    async refreshToken() {
      if (!this.$auth.loggedIn) return
      const refreshToken = this.$auth.getRefreshToken('local')
      if (!refreshToken) {
        await this.$auth.logout()
        return
      }
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
