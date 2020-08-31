<template>
  <v-card>
    <v-card-text>
      <agent-header />
    </v-card-text>

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
  components: { AgentHeader: () => import('@/components/agent/AgentHeader') },
  data() {
    return {
      options: {
        title: {
          text: 'Registros de usuarios en los últimos 30 días',
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
            ],
          },
        ],
      },
      usersLoaded: false,
    }
  },
  async created() {
    await this.fetchRegistrationsAndCalculos()
    await this.fetchUsers()
  },
  methods: {
    async fetchRegistrationsAndCalculos() {
      const monthAgo = addDays(new Date(), -30)
      const monthAgoStr = format(monthAgo, 'yyyy-MM-dd 00:00')
      const usersData = await this.$axios.$get(
        `users/users/?fields=date_joined_date&ordering=date_joined&date_joined__gte=${monthAgoStr}`,
      )

      const days = eachDayOfInterval({ start: monthAgo, end: new Date() }).map((d) => format(d, 'dd/MM/yyyy'))

      this.options.series = [
        {
          name: `Nuevo usuarios (${usersData.length})`,
          data: days.map((day) => usersData.filter((item) => item.date_joined_date === day).length),
        },
      ]
      this.options.xAxis.categories = days.filter(constants.onlyUnique)
    },
    async fetchUsers() {
      const clients = await this.$axios.$get('users/users/?client_role=client&page=1&itemsPerPage=1')
      const leeds = await this.$axios.$get('users/users/?client_role=leed&page=1&itemsPerPage=1')
      this.usersOptions.series[0].data[0].y = clients.count
      this.usersOptions.series[0].data[1].y = leeds.count
      this.usersLoaded = Boolean(clients.count || leeds.count)
    },
  },
}
</script>
