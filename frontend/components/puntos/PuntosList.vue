<template>
  <div>
    <div v-for="punto in puntos" :key="punto.id">
      <v-card-title> Punto suministro {{ punto.name || `(id: ${punto.id})` }} </v-card-title>
      <v-card-text>
        <v-row>
          <v-col v-for="field in puntoHeaders" :key="field.value" style="min-width: 30%;">
            <div v-if="field.value !== 'company_luz' && !editable">
              <span> {{ field.name }}: </span>
            </div>
            <v-spacer />
            <div>
              <company-select
                v-if="editable && field.value === 'company_luz'"
                :value="punto.company_luz"
                @input="
                  save({
                    id: punto.id,
                    field: 'company_luz',
                    value: $event,
                  })
                "
              />
              <v-text-field
                v-else-if="editable"
                :label="field.name"
                :value="punto[field.value]"
                append-icon="mdi-content-save"
                @input="values[field.value] = $event"
                @click:append="save({ id: punto.id, field: field.value })"
              />
              <code v-else>
                {{ punto[field.value] || '-' }}
              </code>
            </div>
          </v-col>
        </v-row>
      </v-card-text>

      <v-card-title>
        Archivos adjuntos:
        {{ punto.attachments.length ? '' : '...' }}
      </v-card-title>
      <v-card-text v-if="punto.attachments.length">
        <v-chip
          v-for="attachment in punto.attachments"
          :key="attachment.id"
          link
          exact
          target="_blank"
          :href="attachment.attachment"
        >
          {{ attachment.type_verbose_name }}
        </v-chip>
      </v-card-text>

      <v-divider :key="punto.id" />
    </div>
  </div>
</template>

<script>
export default {
  name: 'PuntosList',
  components: {
    CompanySelect: () => import('~/components/selects/CompanySelect'),
  },
  props: {
    editable: {
      type: Boolean,
      default: false,
    },
    puntos: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      values: {},
    }
  },
  computed: {
    puntoHeaders() {
      const isAdmin = this.$auth.user.role === 'admin'
      return this.$store.state.puntoHeaders.filter((h) => {
        return !(!isAdmin && ['c1', 'c2', 'c3'].includes(h.value))
      })
    },
  },
  async created() {
    if (!this.puntoHeaders || !this.puntoHeaders.length) {
      this.$store.commit('setPuntoHeaders', await this.$axios.$get('/users/puntos/get_headers/'))
    }
  },
  methods: {
    async save({ id, field, value }) {
      const data = {}
      value = value === undefined ? null : value
      data[field] = value || this.values[field]
      try {
        await this.$axios.$patch(`users/puntos/${id}/`, data)
        await this.$swal({
          title: 'Salvado',
          text: `${field.toUpperCase()} esta cambiado ${value || this.values[field] || 'null'}`,
          icon: 'success',
        })
        this.$emit('punto-updated')
      } catch (e) {
        const errorMsg = e.response.data
        await this.$swal({
          title: 'Error!',
          text: errorMsg[field] instanceof Array ? errorMsg[field].join(',') : JSON.stringify(errorMsg),
          icon: 'error',
        })
      }
    },
  },
}
</script>
