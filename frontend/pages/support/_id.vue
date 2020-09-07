<template>
  <v-card>
    <v-card-text v-if="$auth.user.role === 'admin'">
      <admin-header />
    </v-card-text>

    <v-card-text>
      <user-detail-data :user="values" />
    </v-card-text>

    <v-divider />

    <v-card-title>Solicitudes</v-card-title>
    <v-card-text>
      <v-list>
        <v-list-group v-for="bid in user.bids" :key="bid.id" v-model="bid.active" no-action>
          <template v-slot:activator>
            <v-list-item-content>
              ID: {{ bid.id }}

              <v-chip :color="bidStatusColor(bid.status)">
                {{ bid.status }}
              </v-chip>
            </v-list-item-content>
          </template>

          <v-list-item>
            <v-list-item-content>
              <tramitacion :bid-id="bid.id" @tramitate="bid.status = $event" />
            </v-list-item-content>
          </v-list-item>
        </v-list-group>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  components: {
    AdminHeader: () => import('~/components/admin/AdminHeader'),
    UserDetailData: () => import('@/components/forms/UserDetailData'),
    Tramitacion: () => import('~/components/support/Tramitacion'),
  },
  async asyncData({ $axios, params }) {
    const user = await $axios.$get(`users/users/${params.id}/`)

    return {
      user,
      values: {
        first_name: user.first_name,
        last_name: user.last_name,
        phone: user.phone,
        email: user.email,
        dni: user.dni,
        iban: user.iban,
        cif_dni: user.cif_dni,
        phones: [user.phone],
      },
    }
  },
  data() {
    return {
      cols: 3,
      errorMessages: { status: null, message: null },
    }
  },
  methods: {
    bidStatusColor(status) {
      let color
      switch (status) {
        case 'OK':
          color = 'success'
          break
        case 'Pendiente tramitacion':
          color = 'warning'
          break
        default:
          color = 'error'
          break
      }
      return color
    },
    async refresh() {
      this.user = await this.$axios.$get(`users/users/${this.user.id}/`)
    },
    async update({ field }) {
      const data = {}
      let value = this.values[field]
      value = value === undefined ? null : value
      data[field] = value
      try {
        await this.$axios.$patch(`users/users/${this.bid.user.id}/`, data)
        this.bid = await this.$axios.$get(`bids/bids/${this.bid.id}?support=true`)
        await this.$swal({
          title: 'Salvado',
          text: `${field.toUpperCase()} esta cambiado ${data[field]}`,
          icon: 'success',
        })
      } catch (e) {
        await this.$swal({
          title: 'Error!',
          text: e.response.data[field] ? e.response.data[field].join(', ') : JSON.parse(e.response.data),
          icon: 'error',
        })
      }
    },
  },
}
</script>
