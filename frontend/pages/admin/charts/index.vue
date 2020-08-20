<template>
  <v-card>
    <v-card-text>
      <admin-header />
    </v-card-text>

    <v-card-text>
      <highchart :options="options" />
    </v-card-text>
  </v-card>
</template>

<script>
function onlyUnique(value, index, self) {
  return self.indexOf(value) === index
}
import { eachDayOfInterval, addDays, format } from 'date-fns'
export default {
  components: { AdminHeader: () => import('@/components/admin/AdminHeader') },
  data() {
    return {
      options: {
        title: {
          text: 'Registros de usuarios y calculos en los últimos 30 días',
        },
        xAxis: {
          categories: [],
        },
        yAxis: {
          title: {
            text: 'Quantity',
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
    }
  },
  async mounted() {
    const monthAgo = addDays(new Date(), -30)
    const monthAgoStr = format(monthAgo, 'yyyy-MM-dd 00:00')
    const usersData = await this.$axios.$get(
      `users/users/?fields=date_joined_date&ordering=date_joined&date_joined__gte=${monthAgoStr}`,
    )
    const logsData = await this.$axios.$get(`users/logs/?requested_at__gte=${monthAgoStr}`)

    const days = eachDayOfInterval({ start: monthAgo, end: new Date() }).map((d) => format(d, 'dd/MM/yyyy'))

    this.options.series = [
      {
        name: `Nuevo usuarios (${usersData.length})`,
        data: days.map((day) => usersData.filter((item) => item.date_joined_date === day).length),
      },
      {
        name: `Calculos (${logsData.length})`,
        data: days.map((day) => logsData.filter((item) => item.requested_at === day).length),
      },
    ]
    this.options.xAxis.categories = days.filter(onlyUnique)
    // this.options.subtitle.text = `Total: ${usersData.length} usuarios y ${logsData.length} calculos`
  },
}
</script>
