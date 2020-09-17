<template>
  <v-card>
    <v-card-text>
      <v-row>
        <v-col>
          <vue-ctk-date-time-picker
            v-model="datesFilter"
            label="Fechas"
            format="YYYY-MM-DD HH:mm"
            formatted="DD/MM/YYYY HH:mm"
            range
            color="indigo"
            :dark="$vuetify.theme.isDark"
          />
        </v-col>

        <v-col>
          <v-autocomplete
            v-model="agentsFilter"
            label="Agentes"
            :items="$store.state.responsibles"
            outlined
            item-text="fullname"
            item-value="id"
            multiple
            clearable
          />
        </v-col>
      </v-row>
    </v-card-text>

    <v-divider />

    <v-card-text>
      <highchart :options="chartOptions" />
    </v-card-text>

    <v-divider />

    <v-card-text> clients table </v-card-text>
  </v-card>
</template>

<script>
import constants from '@/lib/constants'
import { format } from 'date-fns'
export default {
  data() {
    const today = format(new Date(), 'yyyy-MM-dd HH:mm')
    return {
      datesFilter: { start: today, end: today },
      agentsFilter: [],
      chartOptions: {
        title: {
          text: '',
        },
        xAxis: {
          categories: [],
        },
        yAxis: {
          title: {
            text: '',
          },
          step: 1,
        },
        series: [
          {
            data: [],
          },
        ],
      },
    }
  },
  watch: {
    async datesFilter() {
      await this.refresh()
    },
    async agentsFilter() {
      await this.refresh()
    },
  },
  async created() {
    await this.$store.dispatch('fetchResponsibles')
    await this.refresh()
  },
  methods: {
    async refresh() {
      const { start, end } = this.datesFilter
      const clients = await this.$axios.$get(
        `users/users/?fields=responsible,date_joined_date,status&ordering=date_joined&date_joined__range=${start},${end}&responsible__in=${this.agentsFilter.join(
          ',',
        )}`,
      )
      this.chartOptions.xAxis.categories = clients.map((c) => c.date_joined_date).filter(constants.onlyUnique)
      this.chartOptions.series[0].data = this.chartOptions.xAxis.categories.map(
        (date) => clients.filter((c) => c.date_joined_date === date).length,
      )
    },
  },
}
</script>
