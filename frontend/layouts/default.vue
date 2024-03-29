<template>
  <v-app>
    <v-navigation-drawer v-if="$auth.loggedIn" v-model="drawer" fixed app clipped>
      <v-list>
        <v-list-item v-for="(item, i) in items" :key="i" :href="item.href" :to="item.to" nuxt>
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

      <notys v-if="$auth.user.role" />

      <v-btn icon nuxt to="/profile">
        <v-icon color="primary"> mdi-account </v-icon>
      </v-btn>

      <theme-switcher />

      <v-btn v-if="$auth" icon @click.stop="$auth.logout">
        <v-icon color="primary"> mdi-logout </v-icon>
      </v-btn>
    </v-app-bar>
    <v-main>
      <nuxt />
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'Default',
  components: {
    Notys: () => import('@/components/notys'),
    ThemeSwitcher: () => import('~/components/ThemeSwitcher'),
  },
  data() {
    return {
      drawer: true,
      title: this.$vuetify.breakpoint.mobile ? '' : 'Gestion Group',
    }
  },
  computed: {
    items() {
      let items = []
      const user = this.$auth.user
      const { permissions, role } = user
      if (role === 'admin') {
        items = items.concat([
          {
            icon: 'mdi-monitor-dashboard',
            title: 'DASHBOARD',
            to: '/admin/dashboard',
          },
          {
            icon: 'mdi-file-document-edit',
            title: 'TRAMITACIÓN',
            to: '/admin/tramitacion',
          },
          {
            icon: 'mdi-file-cancel-outline',
            title: 'PAPELERA',
            to: '/admin/ko',
          },
          {
            icon: 'mdi-briefcase-account-outline',
            title: 'CLIENTES',
            to: '/admin/clientes',
          },
          {
            icon: 'mdi-account-tie',
            title: 'USUARIOS',
            to: '/admin/usuarios',
          },
          {
            icon: 'mdi-table',
            title: 'OFERTAS COMPARADOR',
            to: '/admin/ofertas_comparador',
          },
          {
            icon: 'mdi-table',
            title: 'OFERTAS TRAMITACIÓN',
            to: '/admin/ofertas_tramitacion',
          },
          {
            icon: 'mdi-math-log',
            title: 'HISTORIAL',
            to: '/admin/log',
          },
        ])
      } else if (role === 'agent') {
        items = items.concat([
          {
            icon: 'mdi-account-plus',
            title: 'NUEVO CLIENTE',
            to: '/agente/nuevo_cliente',
          },
          {
            icon: 'mdi-file-document-edit',
            title: 'TRAMITACIÓN',
            to: '/agente/tramitacion',
          },
          {
            icon: 'mdi-call-merge',
            title: 'Call&Visit',
            href: 'https://call-visit.gestiongroup.es',
          },
        ])
        if (user.agent_type === 'canal') {
          items.splice(3, 0, {
            icon: 'mdi-account-multiple',
            title: 'AGENTES',
            to: '/agente/agentes',
          })
        }
      } else if (role === 'support') {
        items = [
          {
            icon: 'mdi-lifebuoy',
            title: 'TRAMITACIÓN',
            to: '/admin/tramitacion',
          },
          {
            icon: 'mdi-file-cancel-outline',
            title: 'PAPELERA',
            to: '/admin/ko',
          },
          {
            icon: 'mdi-briefcase-account-outline',
            title: 'CLIENTES',
            to: '/admin/clientes',
          },
        ]
      } else {
        items = items.concat([
          {
            icon: 'mdi-briefcase',
            title: 'Cartera',
            to: '/bids',
          },
          {
            icon: 'mdi-account-tie',
            title: 'Asistente personal',
            to: '/assistant',
          },
        ])
      }
      if (permissions.includes('calculator')) {
        items.push({ icon: 'mdi-calculator', title: 'COMPARADOR', to: '/comparador' })
      }
      if (role) {
        items.push({ icon: 'mdi-information', title: 'INFO', to: '/info' })
      }
      return items
    },
  },
}
</script>
