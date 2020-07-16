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
            <v-icon color="primary">{{ item.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title v-text="item.title" />
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar fixed app v-if="$auth.loggedIn" clipped-left>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" color="primary" />
      <v-toolbar-title v-text="title" />
      <v-spacer />

      <v-btn icon nuxt to="/profile">
        <v-icon color="primary">
          mdi-account
        </v-icon>
      </v-btn>

      <theme-switcher />
      <v-btn v-if="$auth" icon @click.stop="$auth.logout">
        <v-icon color="primary">mdi-logout</v-icon>
      </v-btn>
    </v-app-bar>
    <v-main>
      <v-breadcrumbs
        v-if="!['index', 'login', 'calculator'].includes($route.name)"
        :items="breadcrumbs"
        large
      >
        <template v-slot:item="{ item }">
          <v-breadcrumbs-item :to="item.to" replace exact>{{
            item.text
          }}</v-breadcrumbs-item>
        </template>
      </v-breadcrumbs>
      <nuxt />
      <chat v-if="showChat" :participant="participant" />
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
  async created() {
    if (!this.$auth.user) return
    const role = this.$auth.user.role
    if (role === null) {
      const p = await this.$axios.$get('chat/messages/get_participant/')
      this.$store.commit('setParticipant', p)
    }
  },
  computed: {
    participant() {
      return this.$store.state.participant
    },
    showChat() {
      return (
        this.$auth.user &&
        this.$auth.user.role === null &&
        this.participant &&
        this.participant.id
      )
    },
    breadcrumbs() {
      const crumbs = this.$route.path.split('/')
      return crumbs.map((crumb, idx) => {
        const crumbPath = crumbs.filter((c1, idx1) => idx1 <= idx).join('/')
        const match = this.$router.match(crumbPath)
        return {
          text: crumb,
          to: { params: match.params, name: match.name, query: match.query },
        }
      })
    },
    items() {
      const items = []
      if (this.$auth.user.permissions.includes('offers')) {
        items.push({
          icon: 'mdi-offer',
          title: 'Ofertas',
          to: '/offers',
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
          title: 'Soporte',
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
  },
}
</script>
