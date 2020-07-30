<template>
  <v-card-text>
    <v-card-title>Ofertas (totales: {{ total }})</v-card-title>
    <v-card-text>
      <v-row align="center">
        <v-col>
          <v-select
            v-model="filters.is_price_permanent"
            label="Tipo de precio"
            :items="
              ['Fijo', 'Indexado'].map((i) => {
                return {
                  text: i,
                  value: i,
                }
              })
            "
            @input="$emit('filters-updated', filters)"
          />
        </v-col>
        <v-col>
          <company-select
            v-model="filters.company"
            without-other
            @input="$emit('filters-updated', filters)"
          />
        </v-col>
        <v-col>
          <tarif-select
            v-model="filters.tarif"
            @input="$emit('filters-updated', filters)"
          />
        </v-col>
      </v-row>
    </v-card-text>
  </v-card-text>
</template>
<script>
export default {
  name: 'OffersListToolbar',
  components: {
    TarifSelect: () => import('~/components/selects/TarifSelect'),
    ClientTypeSelect: () => import('~/components/selects/ClientTypeSelect'),
    CompanySelect: () => import('~/components/selects/CompanySelect'),
  },
  props: {
    defaultFilters: {
      type: Object,
      default: () => {},
    },
    total: {
      type: Number,
      default: 0,
    },
  },
  data() {
    return {
      filters: this.defaultFilters,
    }
  },
}
</script>
