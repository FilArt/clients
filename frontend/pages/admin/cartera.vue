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
import { format, addDays } from 'date-fns'
export default {
  data() {
    const fdates = [addDays(new Date(), -30), new Date()].map((d) => format(d, 'yyyy-MM-dd HH:mm'))
    return {
      datesFilter: { start: fdates[0], end: fdates[1] },
      agentsFilter: [],
      chartOptions: {
        chart: {
          // plotBackgroundColor: null,
          // plotBorderWidth: null,
          // plotShadow: false,
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
            name: 'Estados por clientes',
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
        )}&role__isnull=true`,
      )
      this.chartOptions.xAxis.categories = clients.map((c) => c.status).filter(constants.onlyUnique)
      this.chartOptions.series[0].data = this.chartOptions.xAxis.categories.map(
        (status) => clients.filter((c) => c.status === status).length,
      )
    },
  },
}
</script>
