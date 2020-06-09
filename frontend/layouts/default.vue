<template>
  <v-app dark>
    <v-navigation-drawer
      v-if="$auth.loggedIn"
      v-model="drawer"
      :mini-variant="miniVariant"
      :clipped="clipped"
      fixed
      app
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
    <v-app-bar :clipped-left="clipped" fixed app v-if="$auth.loggedIn">
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-btn icon @click.stop="miniVariant = !miniVariant">
        <v-icon>mdi-{{ `chevron-${miniVariant ? 'right' : 'left'}` }}</v-icon>
      </v-btn>
      <v-btn icon @click.stop="clipped = !clipped">
        <v-icon>mdi-application</v-icon>
      </v-btn>
      <v-btn icon @click.stop="fixed = !fixed">
        <v-icon>mdi-minus</v-icon>
      </v-btn>
      <v-toolbar-title v-text="title" />
      <v-spacer />
      <v-btn v-if="$auth" icon @click.stop="$auth.logout">
        <v-icon>mdi-logout</v-icon>
      </v-btn>
    </v-app-bar>
    <v-content>
      <v-container>
        <nuxt />
      </v-container>
    </v-content>
    <v-footer :fixed="fixed" app>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: 'Default',
  data() {
    return {
      clipped: false,
      drawer: false,
      fixed: false,
      items: [
        {
          icon: 'mdi-account',
          title: 'Profile',
          to: '/profile'
        },
        {
          icon: 'mdi-briefcase',
          title: 'Bids',
          to: '/bids'
        },

        {
          icon: 'mdi-calculator',
          title: 'Calculator',
          to: '/calculator'
        },
        {
          icon: 'mdi-offer',
          title: 'Offers',
          to: '/offers'
        },
        {
          icon: 'mdi-cog',
          title: 'Settings',
          to: '/settings'
        }
      ],
      miniVariant: false,
      title: 'Vuetify.js'
    }
  },
  async mounted() {
    const refreshToken = this.$auth.getRefreshToken('local')
    if (!refreshToken) return
    const responseData = await this.$axios.$post('users/refresh', {
      refresh: refreshToken
    })
    this.$auth.setToken('local', 'Bearer ' + responseData.access)
  }
}
</script>
