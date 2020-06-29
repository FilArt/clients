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

      <template v-slot:append>
        <small>Last update: 28/06/2020 3:00</small>
      </template>
    </v-navigation-drawer>

    <v-app-bar fixed app v-if="$auth.loggedIn" clipped-left>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" color="primary" />
      <v-toolbar-title v-text="title" />
      <v-spacer />
      <theme-switcher />
      <v-btn v-if="$auth" icon @click.stop="$auth.logout">
        <v-icon color="primary">mdi-logout</v-icon>
      </v-btn>
    </v-app-bar>
    <v-main>
      <v-breadcrumbs
        v-if="!['index', 'login'].includes($route.name)"
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
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'Default',
  components: { ThemeSwitcher: () => import('~/components/ThemeSwitcher') },
  data() {
    return {
      drawer: true,
      title: 'Gestion Group',
    }
  },
  computed: {
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
      items.push({
        icon: 'mdi-account',
        title: 'Perfil',
        to: '/profile',
      })

      const role = this.$auth.user.role
      if (role === 'support') {
        items.push({
          icon: 'mdi-lifebuoy',
          title: 'Soporte',
          to: '/support',
        })
      }
      return items
    },
  },
}
</script>
