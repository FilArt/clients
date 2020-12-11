<template>
  <v-card>
    <v-card-text>
      <add-new-client-dialog />
    </v-card-text>

    <v-card-text>
      <v-row>
        <v-col>
          <v-progress-linear v-show="loading" indeterminate />
        </v-col>
      </v-row>
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

    <v-card-text>
      <highchart :options="chartOptions" />
    </v-card-text>

    <v-divider />

    <v-card-text>
      <highchart :options="options" />
    </v-card-text>

    <v-card-text v-if="usersLoaded">
      <highchart :options="usersOptions" />
    </v-card-text>
  </v-card>
</template>

<script>
import { eachDayOfInterval, addDays, format } from 'date-fns'
import constants from '@/lib/constants'
export default {
  components: {
    AddNewClientDialog: () => import('@/components/dialogs/AddNewClientDialog'),
    DateTimeFilter: () => import('~/components/DateTimeFilter'),
  },
  data() {
    const fdates = [addDays(new Date(), -30), new Date()].map((d) => format(d, 'yyyy-MM-dd HH:mm'))
    return {
      loading: false,
      fechaRegistro: { start: fdates[0], end: fdates[1] },
      fechaFirma: { start: null, end: null },
      agentsFilter: [],
      chartOptions: {
        chart: {
          // backgroundColor: 'yellow',
          // plotBackgroundColor: 'indigo',
          plotBorderWidth: 1,
          plotShadow: true,
          type: 'bar',
        },
        title: {
          text: 'Estados',
        },
        xAxis: {
          categories: [],
        },
        yAxis: {
          title: {
            text: 'Cantidad',
          },
          step: 1,
        },
        series: [
          {
            name: 'Fichas',
            data: [],
          },
        ],
      },
      options: {
        title: {
          text: 'Registros de usuarios y calculos en los últimos 30 días',
        },
        xAxis: {
          categories: [],
        },
        yAxis: {
          title: {
            text: 'Número',
          },
        },
        series: [
          {
            data: [],
          },
          {
            data: [],
          },
        ],
      },
      usersOptions: {
        chart: {
          plotBackgroundColor: null,
          plotBorderWidth: null,
          plotShadow: false,
          type: 'pie',
        },
        tooltip: {
          pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>',
        },
        accessibility: {
          point: {
            valueSuffix: '%',
          },
        },
        plotOptions: {
          pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
              enabled: true,
              format: '<b>{point.name}</b>: {point.y}',
            },
          },
        },
        title: {
          text: 'Análisis de usuario',
        },
        series: [
          {
            name: 'Usuarios',
            colorByPoint: true,
            data: [
              {
                name: 'Clientes',
                sliced: true,
                selected: true,
              },
              {
                name: 'Leeds',
              },
              {
                name: 'Visitors',
              },
            ],
          },
        ],
      },
      usersLoaded: false,
    }
  },

  async created() {
    await this.$store.dispatch('fetchResponsibles')
    await this.refresh()

    await this.fetchRegistrationsAndCalculos()
    await this.fetchUsers()
  },

  methods: {
    async refresh() {
      this.loading = true
      const params = {
        responsible__in: this.agentsFilter.join(','),
        role__isnull: true,
        statuses_in: [...Object.values(constants.statuses)],
        ordering: 'date_joined',
        fields: 'status,bids_count',
      }
      if (this.fechaRegistro && this.fechaRegistro.end) {
        const { start, end } = this.fechaRegistro
        params.date_joined__range = `${start},${end}`
      }
      if (this.fechaFirma && this.fechaFirma.end) {
        const { start, end } = this.fechaFirma
        params.fecha_firma__range = `${start},${end}`
      }
      const paramsStr = Object.keys(params)
        .map((k) => k + '=' + params[k])
        .join('&')
      try {
        const totalName = 'TOTAL CLIENTES'
        const totalBidName = 'TOTAL SOLICITUDES'
        const clients = await this.$axios.$get(`users/users/?${paramsStr}`)
        this.chartOptions.xAxis.categories = clients
          .map((c) => c.status)
          .filter(constants.onlyUnique)
          .concat([totalName, totalBidName])
        this.chartOptions.series[0].data = this.chartOptions.xAxis.categories.map((status) =>
          status === totalBidName
            ? clients.map((c) => c.bids_count).reduce((a, b) => a + b)
            : status === totalName
            ? clients.length
            : clients.filter((c) => c.status === status).length,
        )
      } finally {
        this.loading = false
      }
    },
    async fetchRegistrationsAndCalculos() {
      const monthAgo = addDays(new Date(), -30)
      const monthAgoStr = format(monthAgo, 'yyyy-MM-dd 00:00')
      const usersData = await this.$axios.$get(
        `users/users/?fields=date_joined&ordering=date_joined&date_joined__gte=${monthAgoStr}`,
      )
      const logsData = await this.$axios.$get(`users/logs/?fields=requested_at&requested_at__gte=${monthAgoStr}`)

      const days = eachDayOfInterval({ start: monthAgo, end: new Date() }).map((d) => format(d, 'dd/MM/yyyy'))

      this.options.series = [
        {
          name: `Nuevo usuarios (${usersData.length})`,
          data: days.map((day) => usersData.filter((item) => item.date_joined === day).length),
        },
        {
          name: `Calculos (${logsData.length})`,
          data: days.map((day) => logsData.filter((item) => item.requested_at === day).length),
        },
      ]
      this.options.xAxis.categories = days.filter(constants.onlyUnique)
      // this.options.subtitle.text = `Total: ${usersData.length} usuarios y ${logsData.length} calculos`
    },
    async fetchUsers() {
      const clientsStatuses = [...Object.values(constants.statuses.client)].join(',')
      const clients = await this.$axios.$get(`users/users/?statuses_in=${clientsStatuses}&page=1&itemsPerPage=1`)
      const leeds = await this.$axios.$get(`users/users/?statuses_in=${constants.statuses.LEED}&page=1&itemsPerPage=1`)
      const visitorsCount = (await this.$axios.$get('users/logs/?fields=remote_addr&distinct=remote_addr'))
        .map((i) => i.remote_addr)
        .filter(constants.onlyUnique).length
      this.usersOptions.series[0].data[0].y = clients.count
      this.usersOptions.series[0].data[1].y = leeds.count
      this.usersOptions.series[0].data[2].y = visitorsCount
      this.usersLoaded = true
    },
  },
}
</script>
