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

export default {
  components: { AdminHeader: () => import('@/components/admin/AdminHeader') },
  data() {
    return {
      options: {
        title: {
          text: 'Registrations',
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
            name: 'Nuevo usuarios',
            data: [],
          },
          {
            name: 'Calculos',
            data: [],
          },
        ],
      },
    }
  },
  async mounted() {
    const usersData = await this.$axios.$get('users/users/?fields=date_joined_date&ordering=date_joined')
    const logsData = await this.$axios.$get('users/logs/')

    const userDays = usersData.map((item) => item.date_joined_date).filter(onlyUnique)
    const logsDays = logsData.map((item) => item.requested_at).filter(onlyUnique)
    const days = userDays.concat(logsDays)

    this.options.series[0].data = days.map((day) => usersData.filter((item) => item.date_joined_date === day).length)
    this.options.series[1].data = days.map((day) => logsData.filter((item) => item.requested_at === day).length)
    this.options.xAxis.categories = days.filter(onlyUnique)
  },
}
</script>
