<template>
  <vue-ctk-date-time-picker
    :id="label"
    v-model="dateTime"
    :label="label"
    :format="format"
    :formatted="formatted"
    :range="range"
    :color="color"
    :inline="inline"
    :dark="$vuetify.theme['isDark']"
    :custom-shortcuts="customShortcuts"
    button-now-translation="Ahora"
    auto-close
    @input="$emit('input', $event)"
  />
</template>
<script>
export default {
  name: 'DateTimeFilter',
  props: {
    value: {
      type: [String, Object],
      default: () => null,
    },
    label: {
      type: String,
      default: 'Fechas',
    },
    format: {
      type: String,
      default: 'YYYY-MM-DD HH:mm',
    },
    formatted: {
      type: String,
      default: 'DD/MM/YYYY HH:mm',
    },
    color: {
      type: String,
      default: 'purple',
    },
    range: {
      type: Boolean,
      default: false,
    },
    inline: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      dateTime: this.getValue(this.value),
      customShortcuts: [
        { key: 'thisWeek', label: 'Esta semana', value: 'isoWeek' },
        { key: 'lastWeek', label: 'Ultima semana', value: '-isoWeek' },
        { key: 'last7Days', label: 'Ultima 7 dias', value: 7 },
        { key: 'last30Days', label: 'Ultima 30 dias', value: 30 },
        { key: 'thisMonth', label: 'Este mes', value: 'month' },
        { key: 'lastMonth', label: 'Último mes', value: '-month' },
        { key: 'thisYear', label: 'Este año', value: 'year' },
        { key: 'lastYear', label: 'Último año', value: '-year' },
      ],
    }
  },
  watch: {
    value: {
      handler(val) {
        this.dateTime = this.getValue(val)
      },
      deep: true,
    },
  },
  methods: {
    getValue(val) {
      if ((val instanceof String || typeof val === 'string') && val.includes(',')) {
        val = val.split(',')
        return { start: val[0], end: val[1] }
      }
      return val
    },
  },
}
</script>
