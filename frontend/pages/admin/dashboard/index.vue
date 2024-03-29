<template>
  <v-card>
    <v-card-text v-if="$auth.user.role === 'admin'">
      <v-btn link to="/admin/agents_analytics"> New analytic </v-btn>
    </v-card-text>

    <v-card-text v-if="loading">
      <v-progress-linear indeterminate />
    </v-card-text>

    <v-card-text>
      <add-new-client-dialog />
    </v-card-text>

    <v-card-text>
      <v-row align="top">
        <v-col>
          <date-time-filter
            v-model="fechaRegistro"
            label="Fecha de registro"
            format="YYYY-MM-DD HH:mm"
            formatted="DD/MM/YYYY HH:mm"
            range
            @input="refresh"
          />
        </v-col>

        <v-col>
          <date-time-filter
            v-model="fechaFirma"
            label="Fecha de firma"
            format="YYYY-MM-DD"
            formatted="DD/MM/YYYY"
            range
            @input="refresh"
          />
        </v-col>

        <v-col>
          <v-autocomplete
            v-model="agentsFilter"
            dense
            label="Agentes"
            :items="$store.state.responsibles"
            outlined
            item-text="fullname"
            item-value="id"
            multiple
            clearable
            @change="refresh"
          />
        </v-col>
      </v-row>
    </v-card-text>

    <v-divider />

    <v-card-text v-if="analytics">
      <v-list v-for="analytic in Object.keys(analytics)" :key="analytic">
        <v-list-item>
          <v-list-item-title>{{ analytic }}</v-list-item-title>
          <v-list-item-subtitle>{{ analytics[analytic] }}</v-list-item-subtitle>
        </v-list-item>
      </v-list>
    </v-card-text>

    <v-card-text v-if="commers">
      <v-data-table :headers="commers.headers" :items="commers.rows"></v-data-table>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  components: {
    AddNewClientDialog: () => import('@/components/dialogs/AddNewClientDialog'),
    DateTimeFilter: () => import('~/components/DateTimeFilter'),
  },
  data() {
    return {
      loading: false,
      analytics: null,
      fechaRegistro: { start: null, end: null },
      fechaFirma: { start: null, end: null },
      agentsFilter: [],
      commers: null,
    }
  },

  async mounted() {
    await this.$store.dispatch('fetchResponsibles')
    await this.refresh()
  },
  methods: {
    async refresh() {
      if (this.loading) return
      this.loading = true
      const params = {}
      if (this.agentsFilter && this.agentsFilter.length) params.responsible__in = this.agentsFilter.join(',')
      if (this.fechaRegistro && this.fechaRegistro.end) {
        const { start, end } = this.fechaRegistro
        params.created_at__range = `${start},${end}`
      }
      if (this.fechaFirma && this.fechaFirma.end) {
        const { start, end } = this.fechaFirma
        params.fecha_firma__range = `${start},${end}`
      }
      const paramsStr = Object.keys(params)
        .map((k) => k + '=' + params[k])
        .join('&')
      try {
        const { stats, commers } = await this.$axios.$get(`users/manage_users/analytic/?${paramsStr}`)
        this.analytics = stats
        this.commers = commers
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
