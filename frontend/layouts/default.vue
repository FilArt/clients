<template>
  <v-app>
    <v-navigation-drawer v-if="$auth.loggedIn" v-model="drawer" fixed app clipped>
      <v-list>
        <v-list-item v-for="(item, i) in items" :key="i" :to="item.to" router exact>
          <v-list-item-action>
            <v-icon color="primary">
              {{ item.icon }}
            </v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar v-if="$auth.loggedIn" fixed app clipped-left>
      <v-app-bar-nav-icon color="primary" @click.stop="drawer = !drawer" />
      <v-toolbar-title v-text="title" />
      <v-spacer />

      <v-chip>
        {{ $auth.user ? 'id ' + $auth.user.id : '' }}
      </v-chip>

      <v-btn icon nuxt to="/profile">
        <v-icon color="primary">
          mdi-account
        </v-icon>
      </v-btn>

      <theme-switcher />
      <v-btn v-if="$auth" icon @click.stop="$auth.logout">
        <v-icon color="primary">
          mdi-logout
        </v-icon>
      </v-btn>
    </v-app-bar>
    <v-main>
      <nuxt />
      <chat v-if="showChat" />
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'Default',
  components: {
    ThemeSwitcher: () => import('~/components/ThemeSwitcher'),
    Chat: () => import('~/components/chat/Chat'),
  },
  data() {
    return {
      drawer: true,
      title: 'Gestion Group',
    }
  },
  computed: {
    items() {
      const items = []
      if (this.$auth.user.permissions.includes('offers')) {
        items.push({
          icon: 'mdi-offer',
          title: 'Ofertas',
          to: '/ofertas',
        })
      }
      if (this.$auth.user.permissions.includes('calculator')) {
        items.push({
          icon: 'mdi-calculator',
          title: 'Comparador',
          to: '/calculator',
        })
      }
      items.push({
        icon: 'mdi-briefcase',
        title: 'Cartera',
        to: '/bids',
      })
      items.push({
        icon: 'mdi-account-tie',
        title: 'Asistente personal',
        to: '/assistant',
      })

      const role = this.$auth.user.role
      if (role === 'support') {
        items.push({
          icon: 'mdi-lifebuoy',
          title: 'Tramitacion',
          to: '/support',
        })
      }
      if (role === 'admin') {
        items.push({
          icon: 'mdi-account-group',
          title: 'Admin',
          to: '/admin',
        })
      }
      return items
    },
    showChat() {
      return this.$auth.loggedIn && !this.$auth.user.role
    },
  },
  async created() {
    if (this.showChat) this.$store.dispatch('chat/fetchParticipant')
  },
}
</script>
